# serialize data to render
# convert objects into data types render function can understand

from rest_framework import serializers
from accounts.models import Account, Wallet, Store, Transaction

class AccountSerializer(serializers.ModelSerializer):
    xpub_key = serializers.CharField(source='wallet.xpub_key', read_only=True)
    wallet_hash = serializers.CharField(source='wallet.wallet_hash', read_only=True)
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    
    class Meta:
        model = Account
        fields = ['username', 'token','xpub_key', 'wallet_hash', 'store_name']

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
        model = Transaction
        fields = '__all__'