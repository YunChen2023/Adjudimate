from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView
from .views import UserView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', UserView.as_view(), name='user'),
]
