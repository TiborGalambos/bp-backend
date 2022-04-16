# Generated by Django 3.2.12 on 2022-04-05 09:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0012_auto_20220405_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observation',
            name='obs_author',
        ),
        migrations.AddField(
            model_name='observation',
            name='author_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='observation',
            name='obs_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 5, 11, 39, 26, 619180)),
        ),
    ]
