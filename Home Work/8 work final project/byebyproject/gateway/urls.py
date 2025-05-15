from django.urls import path
from gateway.views import (
    AuthTypeView,
    ClientRegisterView,
    MarchantRegisterView,
    ClientLoginView,
    MarchantLoginView,LogoutView,
    MarchantDashboardView,
    ClintToMarchantPayment,
    ClintToClientSendMoney,
    MarchantTransactionHistoryView
)

urlpatterns = [
    path('', AuthTypeView.as_view()),
    path('register/client/', ClientRegisterView.as_view()),
    path('register/marchant/', MarchantRegisterView.as_view()),
    path('login/client/', ClientLoginView.as_view()),
    path('login/marchant/', MarchantLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('marchant/dashboard/', MarchantDashboardView.as_view()),
    path('<str:phone_number>/<int:amount>/', ClintToMarchantPayment.as_view()),
    path('clint-to-client/<str:sender_phone>/<int:amount>/', ClintToClientSendMoney.as_view()),
    path('marchant/transaction/',MarchantTransactionHistoryView.as_view())
]
