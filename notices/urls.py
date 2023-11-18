from django.urls import path
from .views import NoticeAPI

urlpatterns = [
    path('', NoticeAPI.as_view(), name='notice'),
]
