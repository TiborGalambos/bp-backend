# Generated by Django 4.0.2 on 2022-03-22 13:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_alter_observationnormal_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observationnormal',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 14, 53, 1, 727115)),
        ),
        migrations.AlterField(
            model_name='observationsimple',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 22, 14, 53, 1, 728112)),
        ),
    ]