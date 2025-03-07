from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),   
    path('credential/', include('credential.urls')),
    path('dashboard/', include('dashboard.urls')),
]
