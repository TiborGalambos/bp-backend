# Generated by Django 3.2.12 on 2022-04-15 09:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0022_auto_20220414_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='obs_place',
            field=models.CharField(default='Nowhere', max_length=200),
        ),
        migrations.AlterField(
            model_name='observation',
            name='obs_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 15, 11, 54, 14, 649459)),
        ),
    ]
