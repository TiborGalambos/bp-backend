# Generated by Django 3.2.12 on 2022-03-28 08:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_auto_20220328_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observationnormal',
            name='obs_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 28, 10, 13, 44, 954759)),
        ),
        migrations.AlterField(
            model_name='observationsimple',
            name='obs_description',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='observationsimple',
            name='obs_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 28, 10, 13, 44, 955757)),
        ),
    ]