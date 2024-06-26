from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .forms import AccountCreationForm, AccountChangeForm
from .models import Account

class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = Account
    list_display = ["email", "username",]

admin.site.register(Account, UserAdmin)