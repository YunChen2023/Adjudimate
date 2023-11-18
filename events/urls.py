from django.urls import path
from .views import EventAPI

urlpatterns = [
    path('', EventAPI.as_view(), name='event'),    
]

