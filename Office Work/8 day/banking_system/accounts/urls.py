# accounts/urls.py
from django.urls import path
from .views import RegisterAccountHolder, RegisterModerator, DepositView, TransferView

urlpatterns = [
    path('register/account_holder/', RegisterAccountHolder.as_view()),
    path('register/moderator/', RegisterModerator.as_view()),
    path('deposit/', DepositView.as_view()),
    path('transfer/', TransferView.as_view()),
]
