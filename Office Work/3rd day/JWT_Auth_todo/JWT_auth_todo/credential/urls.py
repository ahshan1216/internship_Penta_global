from django.urls import path
from .views import SignupView, LoginView, TodoView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', TodoView.as_view(), name='dashboard'),
    path('dashboard/<int:pk>/', TodoView.as_view(), name='dashboard')
    
]
