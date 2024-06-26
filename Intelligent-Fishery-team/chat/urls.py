from django.urls import path
from .views import query

urlpatterns = [
    path('api/v1/query/', query, name='query'),
]
