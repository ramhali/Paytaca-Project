import secrets
import string

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Account(AbstractUser):
    def generate_token(length=16): # identifier of accounts
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for i in range(length))
    
    token = models.CharField(max_length=32, unique=True, editable=False, default=generate_token)
    contact_number = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.username

    def get_wallet_id(self):
        return self.wallet.id if hasattr(self, 'wallet') else None
    
    def get_store_name(self):
        return self.store.store_name if hasattr(self, 'store') else None
    
    
class Wallet(models.Model):
    xpub_key = models.CharField(max_length=255, null=True)
    wallet_hash = models.CharField(max_length=255, null=True)
    account = models.OneToOneField(Account, related_name="wallet", on_delete = models.CASCADE)

    def __str__(self):
        return self.account.username
    
class Store(models.Model):
    store_name = models.CharField(max_length=255, null=False,)
    store_type = models.CharField(max_length=255, null=True,)
    store_url = models.CharField(max_length=255, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account = models.OneToOneField(Account, related_name="store", on_delete=models.CASCADE)

    def __str__(self):
        return self.store_name

# TRANSACTIONS ------------

# For the account model
class Order(models.Model):
    amount_crypto = models.DecimalField(max_digits=12, decimal_places=8, default=0)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    store = models.ForeignKey(Store, related_name="store", on_delete=models.CASCADE)

    def __str__(self):
        return self.account.username


# For global use --tracking
class Transaction(models.Model):
    account_token = models.CharField(max_length=100)
    transaction_token = models.CharField(max_length=100)
    tx_id = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    amount_fiat = models.CharField(max_length=100)
    amount_bch = models.DecimalField(max_digits=12, decimal_places=8, default=0)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()