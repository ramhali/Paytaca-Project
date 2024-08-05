
import paho.mqtt.client as mqtt
import json
import time

from decimal import Decimal, ROUND_HALF_UP

from accounts.models import Transaction


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("transactions/#")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    transaction_token = data.get("token")
    tx_id = data.get("txid")
    recipient = data.get("recipient")
    amount_bch = data.get("value")

    # # Save the message to the database
    # mqtt_message = Transaction(
    #     transaction_token=transaction_token,
    #     tx_id=tx_id,
    #     recipient=recipient,
    #     amount_bch=amount_bch
    # )
    # mqtt_message.save()
    try:
        transaction = Transaction.objects.only('recipient').get(recipient=recipient)

        transaction.transaction_token = transaction_token
        transaction.tx_id = tx_id
        transaction.amount_paid += Decimal(amount_bch/100000000)

        transaction.amount_paid=transaction.amount_paid.quantize(Decimal('1.00000000'), rounding=ROUND_HALF_UP)

        # print(transaction.amount_paid, type(transaction.amount_paid))
        # print(transaction.amount_bch, type(transaction.amount_bch))

        if transaction.amount_paid >= transaction.amount_bch:
            transaction.paid = True
            # print(transaction.paid)
            transaction.save()
        else:
            print("WARAY KABASA")

        transaction.save()

    except Transaction.DoesNotExist:
            print("Transaction with the specified recipient does not exist.")

    print(data)


FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code: {rc}")
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        print(f"Reconnecting in {reconnect_delay} seconds...")
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            print("Reconnected successfully!")
            return
        except Exception as err:
            print(f"{err}. Reconnect failed. Retrying...")

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    print(f"Reconnect failed after {reconnect_count} attempts. Exiting...")

_timestamp = str(int(time.time()))
client = mqtt.Client(transport='websockets', client_id="local101-" + _timestamp, clean_session=False)
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

mqtt_broker_url = 'mqtt.watchtower.cash'
client.connect(mqtt_broker_url, 443, 60)
client.loop_forever()
