# Generated by Django 4.2.6 on 2023-10-27 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('entries', '0001_initial'),
        ('criteria', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('score_id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('run_order', models.PositiveIntegerField()),
                ('comment', models.TextField()),
                ('score_description', models.TextField()),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='criteria.criterion')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='entries.entry')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='users.user')),
            ],
        ),
    ]
