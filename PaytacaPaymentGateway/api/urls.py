from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccountViewAPI.as_view(), name="account-view"),
    #path('register/', views.AccountCreateAPI.as_view(), name="account-create"),
    path('login/', views.AccountLoginAPI.as_view(), name="account-login"),
    path('logout/', views.AccountLogoutAPI.as_view(), name="account-logut"),
    #path('add/', views.addItem),
]