# Generated by Django 3.2.12 on 2022-04-05 18:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0017_auto_20220405_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='obs_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 5, 20, 12, 45, 94263)),
        ),
    ]