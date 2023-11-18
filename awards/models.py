from django.db import models
from events.models import Event

class Award(models.Model):
    award_id = models.AutoField(primary_key=True)
    award_type = models.CharField(max_length=255)
    award_description = models.TextField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='awards')
    