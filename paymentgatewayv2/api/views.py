import requests
from decimal import Decimal

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect

from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
from cashaddress import convert

from accounts.models import Account
from accounts.forms import AccountCreationForm, WalletUpdateForm, StoreCreationForm

from . import serializers

class AccountViewAPI(APIView):
    def get(self, request):
        requestData = request.data
        username = requestData.get("username", None)

        if username is not None:
            user = Account.objects.get(username = username)
            serializer = serializers.AccountSerializer(user)
            return Response(serializer.data)
    
        user = Account.objects.all()
        serializer = serializers.AccountSerializer(user, many=True)
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
            return Response({'username': username, 'status': 'Login Success'})
        else:
            return Response({'status': 'errors', 'errors': 'Login Unsuccessful'})
        
class AccountLogoutAPI(APIView):
    def get(self, request):
        logout(request)
        return Response({'status':'Success'})
    
class WalletUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_form = WalletUpdateForm(request.data)

        if wallet_form.is_valid():
            wallet = wallet_form.save(commit=False)
            wallet.account = request.user
            wallet.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'errors', 'errors': wallet_form.errors})

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


class PayRedirectAPIView(APIView):
    def get(self, request, *args, **kwargs):
        input_params = {key: request.GET.get(key) for key in request.GET.keys()}
        query_string = '?' + '&'.join([f'{key}={value}' for key, value in input_params.items()])
        base_url = reverse('pay')
        redirect_url = f'{base_url}{query_string}'

        return HttpResponseRedirect(redirect_url)


class PayAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all query parameters from the request
        query_params = {key: request.GET.get(key) for key in request.GET.keys()}

        bch_rate = None
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "bitcoin-cash", "vs_currencies": query_params['currency'].lower()})
            response.raise_for_status()
            bch_rate = response.json()["bitcoin-cash"][query_params['currency'].lower()]
        except (requests.exceptions.RequestException, KeyError):
            pass

        # convert total to BCH
        total_bch = Decimal(query_params['amount'])
        if bch_rate is not None:
            total_bch /= round(Decimal(bch_rate), 8)

        query_params["amount_bch"] = total_bch
        query_params["bch_address"] = get_address_from_index(query_params['xpub'], query_params['index'])

        # Return all query parameters in the response
        return Response(query_params)
    

def get_address_from_index(xpub, index):
    wallet = HDWallet(symbol=SYMBOL, use_default_path=False)
    result = wallet.from_xpublic_key(xpub).from_path("m/0/" + str(index)).dumps()
    legacy_format = result['addresses']['p2pkh']
    return convert.to_cash_address(legacy_format)


