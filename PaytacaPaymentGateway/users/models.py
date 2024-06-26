from django.db import models

# Create your models here.    
# class Account(models.Model):
#     user_id = models.AutoField(primary_key=True, null=False, unique=True)
#     email = models.EmailField(max_length=255, null=False, unique=True)
#     username = models.CharField(max_length=255, null=False, unique=True)
#     password = models.CharField(max_length=100, null=False)

#     user_id = models.AutoField(primary_key=True, null=False, unique=True)
#     first_name = models.CharField(max_length=255, null=False)
#     last_name = models.CharField(max_length=255, null=False)
#     email = models.EmailField(max_length=255, null=False, unique=True)
#     username = models.CharField(max_length=255, null=False, unique=True)
#     password = models.CharField(max_length=100, null=False)

#     USERNAME_FIELD = 'email'

#     def __str__(self):
#         return self.username
    
#--- ACCOUNT WALLET ---#
# class Wallet(models.Model):
#     xpub_key = models.CharField(max_length=255, null=True)
#     wallet_hash = models.CharField(max_length=255, null=True)
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)