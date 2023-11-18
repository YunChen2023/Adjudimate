# Generated by Django 4.2.6 on 2023-10-27 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('participants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('award_id', models.AutoField(primary_key=True, serialize=False)),
                ('award_type', models.CharField(choices=[('Student Designer of the Year', 'Student Designer of the Year'), ('Emerging Designer of the Year', 'Emerging Designer of the Year'), ('Rising Star Award', 'Rising Star Award')], max_length=255)),
                ('award_description', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='events.event')),
                ('participants', models.ManyToManyField(related_name='awards', to='participants.participant')),
            ],
        ),
    ]
