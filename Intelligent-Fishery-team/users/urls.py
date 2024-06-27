from django.urls import path
from . import views

urlpatterns = [
    path('users/index/', views.index, name='index'),
    path('users/edit/<str:username>/', views.edit, name='edit'),
    path('users/delete/<str:username>/', views.delete, name='delete'),
]
