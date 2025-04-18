from django.urls import path
from .views import RegisterView,LoginView,DashboardView,BankTransferView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('dashboard/',DashboardView.as_view()),
    path('bank-transfer/',BankTransferView.as_view()),
]