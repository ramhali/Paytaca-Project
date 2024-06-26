from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Account(AbstractUser):
    business_name = models.CharField(max_length=255, default="")
    contact_number = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.username

    def get_wallet_id(self):
        return self.wallet.id if hasattr(self, 'wallet') else None
    
class Wallet(models.Model):
    xpub_key = models.CharField(max_length=255, null=True)
    wallet_hash = models.CharField(max_length=255, null=True)
    account = models.OneToOneField(Account, related_name="wallet", on_delete = models.CASCADE)

    def __str__(self):
        return self.account.username
