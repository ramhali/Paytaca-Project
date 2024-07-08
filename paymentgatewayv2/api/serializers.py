# serialize data to render
# convert objects into data types render function can understand

from rest_framework import serializers
from accounts.models import Account, Wallet, Store, Order

class AccountSerializer(serializers.ModelSerializer):
    wallet_id = serializers.IntegerField(source='wallet.id', read_only=True)
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    
    class Meta:
        model = Account
        fields = ['username', 'token','wallet_id', 'store_name']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['xpub_key', 'wallet_hash']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name', 'store_type', 'store_url', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'