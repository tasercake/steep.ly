# Generated by Django 2.2.2 on 2019-06-22 10:28

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='terrain',
            name='slug',
            field=models.CharField(default=api.models.get_unique_slug, max_length=8, unique=True),
        ),
    ]
