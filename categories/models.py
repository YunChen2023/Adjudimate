from django.db import models
from events.models import Event

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_description = models.TextField(blank=True, null=True)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='categories', default=1)

    def __str__(self):
        return self.category_name
