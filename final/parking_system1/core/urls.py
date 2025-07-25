from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path('users/', UserListCreate.as_view()),
    path('roles/', RoleListCreate.as_view()),
    path('assigns/', AssignListCreate.as_view()),
    path('kycs/', KYCListCreate.as_view()),
    path('complains/', ComplainListCreate.as_view()),
    path('maps/', MapListCreate.as_view()),
    path('parkings/', ParkingListCreate.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUserAPIView.as_view(), name='register'),

]
