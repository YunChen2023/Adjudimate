# Generated by Django 4.2.6 on 2023-11-13 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_category_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]