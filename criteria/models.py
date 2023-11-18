from django.db import models
from events.models import Event

class Criterion(models.Model):
    criterion_id = models.AutoField(primary_key=True)
    criterion_type = models.CharField(max_length=255, blank=True, null=True)
    criterion_description = models.TextField(blank=True, null=True)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='criteria', default=1)

    def __str__(self):
        return self.criterion_type