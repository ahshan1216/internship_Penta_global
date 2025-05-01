from django.urls import path
from todo import views

urlpatterns = [
path('', views.index , name='todo_list'),
path('add/', views.add),
path('update/<int:id>/', views.update_todo, name='update_todo'),
path('delete/<int:id>/', views.delete, name='delete_todo'),
]