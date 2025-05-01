from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.home, name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
]