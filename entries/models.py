from django.db import models
from participants.models import Participant
from categories.models import Category
from django.utils import timezone


class Entry(models.Model):
    entry_id = models.AutoField(primary_key=True)
    entry_name = models.CharField(max_length=255)
    entry_photo = models.ImageField(upload_to='entry_photos/', blank=True, null=True)
    entry_audio = models.FileField(upload_to='entry_audios/', blank=True, null=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    run_order = models.PositiveIntegerField(blank=True, null=True)
    ENTRY_STATUS_CHOICES = [
        ('Pending Review', 'Pending Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    entry_status = models.CharField(
        max_length=255,
        choices=ENTRY_STATUS_CHOICES,
        default='Pending Review',
        blank=True, null=True
    )
    entry_description = models.TextField()
    models_name = models.CharField(max_length=255, blank=True, null=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)   
    def __str__(self):
        return self.entry_name
