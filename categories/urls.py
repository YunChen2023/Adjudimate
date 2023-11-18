from django.urls import path
from .views import CategoryAPI

urlpatterns = [
    path('', CategoryAPI.as_view(), name='category'),
]