# Generated by Django 2.2.2 on 2019-06-23 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_terrain_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='terrain',
            name='options',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
