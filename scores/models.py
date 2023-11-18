from django.db import models
from entries.models import Entry
from users.models import User
from events.models import Event
from criteria.models import Criterion

class Score(models.Model):
    score_id = models.AutoField(primary_key=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)    
    comment = models.TextField(blank=True, null=True)
    score_description = models.TextField(blank=True, null=True)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='scores')
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE, related_name='scores')
    