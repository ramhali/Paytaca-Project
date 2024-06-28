from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect

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
        params = {key: request.GET.get(key) for key in request.GET.keys()}
        query_string = '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
        base_url = reverse('pay')
        redirect_url = f'{base_url}{query_string}'

        return HttpResponseRedirect(redirect_url)


class PayAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all query parameters from the request
        query_params = {key: request.GET.get(key) for key in request.GET.keys()}

        # Return all query parameters in the response
        return Response(query_params)