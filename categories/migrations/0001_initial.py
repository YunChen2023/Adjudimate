# Generated by Django 4.2.6 on 2023-10-26 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255)),
                ('category_description', models.TextField()),
            ],
            options={
                'db_table': 'category',
            },
        ),
    ]
