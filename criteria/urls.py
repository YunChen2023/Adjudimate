from django.urls import path
from .views import CriterionAPI

urlpatterns = [
    path('', CriterionAPI.as_view(), name='criterion'),
]
