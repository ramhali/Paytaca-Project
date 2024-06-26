from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account, Wallet

class AccountCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ("username", "business_name")

class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ("username", "business_name")

class WalletUpdateForm(forms.ModelForm):
    xpub_key = forms.CharField()

    class Meta:
        model = Wallet
        fields = ('xpub_key',)