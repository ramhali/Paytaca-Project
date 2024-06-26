from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreationForm, AccountChangeForm
from .models import Account, Wallet

class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = Account
    list_display = ["username", "business_name", "get_wallet_id"]

    def get_wallet_id(self, obj):
        return obj.get_wallet_id()
    
    get_wallet_id.short_description = 'Wallet ID'

admin.site.register(Account, AccountAdmin)
admin.site.register(Wallet)