from django.urls import path
from .views import ScoreEachEntryView
from .views import PlacementView
from .views import TieAlertView
from .views import CommentEachEntryView

urlpatterns = [
    path('mark/', ScoreEachEntryView.as_view(), name='score-each-entry'),
    path('comment/', CommentEachEntryView.as_view(), name='comment-each-entry'),
    path('placement/', PlacementView.as_view(), name='placement'),
    path('tie-alert/', TieAlertView.as_view(), name='tie-alert'),
]
