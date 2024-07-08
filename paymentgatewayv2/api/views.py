import requests
import random

from decimal import Decimal
from queue import Queue

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
from cashaddress import convert

from accounts.models import Account, Wallet, Store, Order, Transaction
from accounts.forms import AccountCreationForm, WalletUpdateForm, StoreCreationForm

from . import serializers

class AccountViewAPI(APIView):
    def get(self, request):
        user = request.user
        account = get_object_or_404(Account, username=user)
        
        serializer = serializers.AccountSerializer(account)
        return Response(serializer.data)

        

class AccountCreateAPI(APIView):        
    @csrf_exempt
    def post(self, request):
        form = AccountCreationForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'errors', 'errors': form.errors})


class AccountLoginAPI(APIView):
    def post(self, request):
        requestData = request.data
        username = requestData.get("username", None)
        password = requestData.get("password", None)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({'username': username, 'status': 'Login Success'})
        else:
            return Response({'status': 'errors', 'errors': 'Login Unsuccessful'})
        
class AccountLogoutAPI(APIView):
    def get(self, request):
        logout(request)
        return Response({'status':'Success'})
    

class WalletUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_form = WalletUpdateForm(request.data)

        if wallet_form.is_valid():
            wallet = wallet_form.save(commit=False)
            wallet.account = request.user
            wallet.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'errors', 'errors': wallet_form.errors})

    def get(self, request):
        account = request.user
        wallet = Wallet.objects.filter(account=account)
        
        if wallet.exists():
            serializer = serializers.WalletSerializer(wallet, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'Empty'})
        

class StoreUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]     

    def post(self, request):
        store_form = StoreCreationForm(request.data)

        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.account = request.user
            store.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'errors', 'errors': store_form.errors})

    def get(self, request):
        account = request.user
        store = Store.objects.filter(account=account)
        
        if store.exists():
            serializer = serializers.StoreSerializer(store, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'Empty'})
        

# class OrderViewAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         account = request.user
#         store = Store.objects.filter(account=account)
#         orders = Order.objects.filter(store__in=store)

#         if orders.exists():
#             serializer = serializers.OrderSerializer(orders, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({'status': 'Empty Transaction'})
        

class PayRedirectAPIView(APIView):
    def get(self, request, *args, **kwargs):
        input_params = {key: request.GET.get(key) for key in request.GET.keys()}
        query_string = '?' + '&'.join([f'{key}={value}' for key, value in input_params.items()])
        base_url = reverse('pay')
        redirect_url = f'{base_url}{query_string}'

        return HttpResponseRedirect(redirect_url)


class PayAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all query parameters from the request
        query_params = {key: request.GET.get(key) for key in request.GET.keys()}

        bch_rate = None
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "bitcoin-cash", "vs_currencies": query_params['currency'].lower()})
            response.raise_for_status()
            bch_rate = response.json()["bitcoin-cash"][query_params['currency'].lower()]
        except (requests.exceptions.RequestException, KeyError):
            pass

        # convert total to BCH
        total_bch = Decimal(query_params['amount'])
        if bch_rate is not None:
            total_bch /= round(Decimal(bch_rate))

        token = query_params.get('token')

        if not token:
            return HttpResponseBadRequest("Token is required")
        
        xpub_key = get_xpub_by_token(token)
        index = 1
        address = get_address_from_index(xpub_key, index)
        wallet_hash = get_wallethash_by_token(token)

        # track address
        subscribe_address(address, index, wallet_hash)

        query_params["amount_bch"] = total_bch
        query_params["address"] = address 

        # print(mqtt_container.get_queue_length())

        return Response(query_params)
    

### HELPER FUNCTIONS ###

# class MQTTContainer:
#     def __init__(self):
#         self.queue = Queue()

#     def add_message(self, message):
#         self.queue.put(message)

#     def get_message(self):
#         return self.queue.get()

#     def get_queue_length(self):
#         return self.queue.qsize()
    
# mqtt_container = MQTTContainer()

# Get xpub & wallet hash of account using the token
def get_xpub_by_token(token):
    account = get_object_or_404(Account, token=token)
    wallet = get_object_or_404(Wallet, account=account)

    return wallet.xpub_key

def get_wallethash_by_token(token):
    account = get_object_or_404(Account, token=token)
    wallet = get_object_or_404(Wallet, account=account)

    return wallet.wallet_hash
# ---------------------------------------------------------------

# Generate a random number
def get_random_number():
    return random.randint(0, 2147483)

# Check if the address already exists in database
def if_address_exists(address):
    return Transaction.objects.filter(recipient=address).exists()

# Get a new adress based on xpub and index
def get_address_from_index(xpub, index):
    while True:
        wallet = HDWallet(symbol=SYMBOL, use_default_path=False)
        result = wallet.from_xpublic_key(xpub).from_path("m/0/" + str(index)).dumps()
        legacy_format = result['addresses']['p2pkh']
        
        if not if_address_exists(convert.to_cash_address(legacy_format)):
                return convert.to_cash_address(legacy_format)

# Subscribe address to watchtower
project_id = '2b99ac81-a956-4ca3-9bf1-fc5d7cba0dd1'

def subscribe_address(address, index, wallet_hash):
    url = 'https://watchtower.cash/api/subscription/'
    data = {
        'addresses': {'receiving': address},
        'project_id': project_id,
        'wallet_hash': wallet_hash,
        'address_index': index
    }
    success = False
    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        success = True
    return success


