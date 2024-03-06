from django.urls import path
from rest_framework.routers import DefaultRouter
from wallet.views import WalletAPI

router = DefaultRouter()

urlpatterns = [path("", WalletAPI.as_view())]
