from django.db import models
from events.models import Event

class Notice(models.Model):
    notice_tab = models.CharField(max_length=255)
    notice = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.notice_tab
