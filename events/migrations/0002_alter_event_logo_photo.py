# Generated by Django 4.2.6 on 2023-11-03 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='logo_photo',
            field=models.ImageField(blank=True, null=True, upload_to='events/'),
        ),
    ]
