# Generated by Django 4.2.6 on 2023-11-13 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('criteria', '0003_criterion_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterion',
            name='criterion_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='criterion',
            name='criterion_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
