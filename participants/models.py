from django.db import models
from events.models import Event

class Participant(models.Model):
    PARTICIPANT_STATUS = [
        ('Student', 'Student'),
        ('Emerging', 'Emerging'),
        ('Other', 'Other'),
    ]
    
    participant_role = models.CharField(max_length=20, default='Entrant')
    participant_id = models.AutoField(primary_key=True)
    participant_description = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='participants/', blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    organisation_name = models.CharField(max_length=255, blank=True, null=True)
    participant_status = models.CharField(max_length=255, choices=PARTICIPANT_STATUS, blank=True, null=True)
    email_address = models.EmailField()
    contact_number = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, default='Australia', blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
            
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants', default=1)
