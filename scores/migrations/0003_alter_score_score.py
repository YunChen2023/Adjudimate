# Generated by Django 4.2.6 on 2023-11-09 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0002_remove_score_run_order_alter_score_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]