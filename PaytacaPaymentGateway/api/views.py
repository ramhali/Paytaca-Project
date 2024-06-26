from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer
from users.forms import UserRegisterForm
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AccountViewAPI(APIView):
    def get(self, request):
        requestData = request.data
        username = requestData.get("username", None)

        if username is not None:
            user = User.objects.get(username = username)
            serializer = AccountSerializer(user)
            return Response(serializer.data)
    
        user = User.objects.all()
        serializer = AccountSerializer(user, many=True)
        return Response(serializer.data)

class AccountCreateAPI(APIView):        
    @csrf_exempt
    def post(self, request):
        form = UserRegisterForm(request.data)
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
            return Response({'status': 'errors', 'errors': user.errors})

class AccountLogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({'status':'Success'})