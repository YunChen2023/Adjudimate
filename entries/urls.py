from django.urls import path
from .views import RejectEntryView
from .views import AcceptEntryView
from .views import MaxRunOrderView
from .views import AddModelsView
from .views import EntryView

urlpatterns = [
    path('reject/', RejectEntryView.as_view(), name='reject-entry'),
    path('accept/', AcceptEntryView.as_view(), name='accept-entry'),
    path('max-run-order/', MaxRunOrderView.as_view(), name='max-run-order'),
    path('add-model/', AddModelsView.as_view(), name='add-model'),
    path('', EntryView.as_view(), name='entry'),
    ]
