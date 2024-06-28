# serialize data to render
# convert objects into data types render function can understand

from rest_framework import serializers
from accounts.models import Account, Wallet, Transaction

class AccountSerializer(serializers.ModelSerializer):
    wallet_id = serializers.IntegerField(source='wallet.id', read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'username', 'wallet_id']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'