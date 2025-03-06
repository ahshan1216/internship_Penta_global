from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),   
    path('credential/', include('credential.urls')),
    path('working_process/', include('working_process.urls')),
]
