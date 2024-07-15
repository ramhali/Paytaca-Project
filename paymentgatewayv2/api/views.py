import requests
import random
import json

from decimal import Decimal, ROUND_HALF_UP

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.db.models import Max

from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
from cashaddress import convert

from accounts.models import Account, Wallet, Store, Transaction
from accounts.forms import AccountCreationForm, WalletUpdateForm, StoreCreationForm

from . import serializers

class AccountViewAPI(APIView):
    def get(self, request):
        user = request.user
        account = get_object_or_404(Account, username=user)
        
        serializer = serializers.AccountSerializer(account)
        return Response(serializer.data)

        

class AccountCreateAPI(APIView):        
    @csrf_exempt
    def post(self, request):
        form = AccountCreationForm(request.data)
        if form.is_valid():
            form.save()

            return Response({'status': 'success'})
        else:
            return Response({'status': 'errors', 'errors': form.errors})


class AccountLoginAPI(APIView):
    def post(self, request):
        requestData = request.data
        username = requestData.get("username", None)
        password = requestData.get("password", None)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': username, 'status': 'Login Success'})
        else:
            return Response({'status': 'errors', 'errors': 'Login Unsuccessful'})
        
class AccountLogoutAPI(APIView):
    def get(self, request):
        logout(request)
        return Response({'status':'Success'})
    

class WalletUpdateAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_form = WalletUpdateForm(request.data)

        if wallet_form.is_valid():
            wallet = wallet_form.save(commit=False)
            wallet.account = request.user
            wallet.is_connected = True
            wallet.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'errors', 'errors': wallet_form.errors})

    def put(self, request):
        try:
            wallet = Wallet.objects.get(account=request.user)
        except Wallet.DoesNotExist:
            return Response({'status': 'error', 'message': 'Wallet not found'}, status=404)
        
        wallet_form = WalletUpdateForm(request.data, instance=wallet)

        if wallet_form.is_valid():
            wallet = wallet_form.save(commit=False)
            wallet.account = request.user
            wallet.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'errors', 'errors': wallet_form.errors})
        
    def get(self, request):
        account = request.user
        wallet = Wallet.objects.filter(account=account)
        
        if wallet.exists():
            serializer = serializers.WalletSerializer(wallet, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'Not connected'})
        

class StoreUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]     

    def post(self, request):
        store_form = StoreCreationForm(request.data)

        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.account = request.user
            store.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'errors', 'errors': store_form.errors})

    def put(self, request):
        try:
            store = Store.objects.get(account=request.user)
        except Store.DoesNotExist:
            return Response({'status': 'error', 'message': 'Store not found'}, status=404)
        
        store_form = StoreCreationForm(request.data, instance=store)

        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.account = request.user
            store.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'errors', 'errors': store_form.errors})
        
    def get(self, request):
        account = request.user
        store = Store.objects.filter(account=account)
        
        if store.exists():
            serializer = serializers.StoreSerializer(store, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'Empty'})
        

class OrderViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = request.user

        transaction = Transaction.objects.only('account_token').filter(account_token=account.token)
        if transaction.exists():
            serializer = serializers.OrderSerializer(transaction, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': 'Empty Transaction'})
        

class PayRedirectAPIView(APIView):
    def get(self, request, *args, **kwargs):
        input_params = request.GET.dict()

        bch_rate = None
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "bitcoin-cash", "vs_currencies": input_params['currency'].lower()})
            response.raise_for_status()
            bch_rate = response.json()["bitcoin-cash"][input_params['currency'].lower()]
        except (requests.exceptions.RequestException, KeyError):
            pass

        total_fiat = input_params['amount']
        # convert total to BCH
        total_bch = Decimal(input_params['amount'])
        if bch_rate is not None:
            total_bch /= round(Decimal(bch_rate))

            # round to 8 decimal places
            total_bch = total_bch.quantize(Decimal('1.00000000'), rounding=ROUND_HALF_UP)

            print(total_bch)

        token = input_params.get('token')

        if not token:
            return HttpResponseBadRequest("Token is required")
        
        xpub_key = get_xpub_by_token(token)
        index = get_available_address_index()
        address = get_address_from_index(xpub_key, index)
        wallet_hash = get_wallethash_by_token(token)

        payment_currency = input_params.get('currency')

        # track address
        subscribe_address(address, index, wallet_hash)

        input_params["amount_bch"] = total_bch
        input_params["address"] = address

        # save to database
        mqtt_message = Transaction(
            account_token=token,
            address_index=index,
            recipient=address,
            currency=payment_currency,
            amount_fiat=total_fiat,
            amount_bch=total_bch,
            amount_paid=0
            )
        mqtt_message.save()

        filtered_keys = ['desc', 'amount', 'currency', 'amount_bch', 'address']
        filtered_params = {key: value for key, value in input_params.items() if key in filtered_keys}

        query_string = '?' + '&'.join([f'{key}={value}' for key, value in filtered_params.items()])
        base_url = reverse('pay')
        redirect_url = f'{base_url}{query_string}'

        return HttpResponseRedirect(redirect_url)


class PayAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all query parameters from the request
        query_params = {key: request.GET.get(key) for key in request.GET.keys()}

        # return Response(query_params)
    
        try:
            transaction = Transaction.objects.only('paid').get(recipient=query_params['address'])
            is_address_paid = transaction.paid

            query_params['paid'] = is_address_paid

            return Response(query_params)
        
        except Transaction.DoesNotExist:
            return Response({'status': 'errors'})


# ---------------------------------------------------------------

### HELPER FUNCTIONS ###

# ---------------------------------------------------------------

# Get xpub & wallet hash of account using the token
def get_xpub_by_token(token):
    account = get_object_or_404(Account, token=token)
    wallet = get_object_or_404(Wallet, account=account)

    return wallet.xpub_key

def get_wallethash_by_token(token):
    account = get_object_or_404(Account, token=token)
    wallet = get_object_or_404(Wallet, account=account)

    return wallet.wallet_hash

# ---------------------------------------------------------------

# Get the available index
def get_available_address_index():
    index = Transaction.objects.aggregate(Max('address_index'))['address_index__max'] or 0
    available_index = index+1
    return available_index

# Check if the address already exists in database by using index
def if_index_exists(value):
    return Transaction.objects.filter(address_index=value).exists()

# ----------------------------------------------------------------

# Get a new adress based on xpub and index
def get_address_from_index(xpub, param_index):
    index = param_index
    while True:
        wallet = HDWallet(symbol=SYMBOL, use_default_path=False)
        result = wallet.from_xpublic_key(xpub).from_path(f"m/0/{index}").dumps()
        legacy_format = result['addresses']['p2pkh']
        
        if not if_index_exists(index):
            return convert.to_cash_address(legacy_format)
        
        index = index + 1  # Get a new random index if address exists


# Subscribe address to watchtower
project_id = '2b99ac81-a956-4ca3-9bf1-fc5d7cba0dd1'

def subscribe_address(address, index, wallet_hash):
    url = 'https://watchtower.cash/api/subscription/'
    data = {
        'addresses': {'receiving': address},
        'project_id': project_id,
        'wallet_hash': wallet_hash,
        'address_index': index
    }
    success = False
    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        success = True
    return success

