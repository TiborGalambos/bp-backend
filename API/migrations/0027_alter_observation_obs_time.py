# Generated by Django 3.2.12 on 2022-04-16 20:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0026_alter_observation_obs_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='obs_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 16, 22, 26, 42, 848641)),
        ),
    ]
