from django.urls import path
from .views import ParticipantView

urlpatterns = [
    path('', ParticipantView.as_view(), name='participant'),
]
