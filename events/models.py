from django.db import models

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    final_entry_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    organiser_name = models.CharField(max_length=255, blank=True, null=True)
    organiser_contact = models.CharField(max_length=255, blank=True, null=True)
    logo_photo = models.ImageField(upload_to='events/', blank=True, null=True)
    event_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.event_name

