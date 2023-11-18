from django.db import models

class User(models.Model):
    USER_ROLES = [
        ('Admin', 'Admin'),
        ('Judge', 'Judge'),
        ('Adjudicator', 'Adjudicator'),
    ]

    user_id = models.AutoField(primary_key=True)
    user_role = models.CharField(max_length=255, choices=USER_ROLES, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='users/', blank=True, null=True)
    usr_description = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    organisation_name = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.EmailField()
    contact_number = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, default='Australia')
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    notification = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email_address


