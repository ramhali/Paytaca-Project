from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account, Wallet, Store

class AccountCreationForm(UserCreationForm):
    store_name = forms.CharField(required=True)

    class Meta:
        model = Account
        fields = ("store_name", "username", "password1", "password2",)

    def save(self, commit=True):
        account = super().save(commit=False)
        if commit:
            account.save()
            store_name = self.cleaned_data['store_name']
            Store.objects.create(account=account, store_name=store_name)
        return account

class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('username',)

class WalletUpdateForm(forms.ModelForm):
    xpub_key = forms.CharField()

    class Meta:
        model = Wallet
        fields = ('xpub_key',)

class StoreCreationForm(forms.ModelForm):
    store_name = forms.CharField()
    store_type = forms.CharField()
    store_url = forms.CharField()

    class Meta:
        model = Store
        fields = ('store_name',
                 'store_type',
                 'store_url',
        )