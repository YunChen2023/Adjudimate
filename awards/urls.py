from django.urls import path
from .views import AwardView

urlpatterns = [
    path('', AwardView.as_view(), name='award'),
]
