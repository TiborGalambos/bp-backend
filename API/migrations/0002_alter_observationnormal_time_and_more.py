# Generated by Django 4.0.2 on 2022-03-22 10:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observationnormal',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 11, 35, 59, 552185)),
        ),
        migrations.AlterField(
            model_name='observationsimple',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 11, 35, 59, 553214)),
        ),
    ]
