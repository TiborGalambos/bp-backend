# Generated by Django 3.2.12 on 2022-04-04 20:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0007_auto_20220404_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obs_author_name', models.CharField(default='username', max_length=150)),
                ('obs_x_coords', models.FloatField(default=0)),
                ('obs_y_coords', models.FloatField(default=0)),
                ('bird_name', models.CharField(max_length=150)),
                ('bird_count', models.IntegerField(default=1)),
                ('obs_time', models.DateTimeField(default=datetime.datetime(2022, 4, 4, 22, 9, 5, 385895))),
                ('bird_photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('bird_size', models.CharField(default=None, max_length=70, null=True)),
                ('obs_description', models.CharField(default=None, max_length=300, null=True)),
                ('obs_is_simple', models.BooleanField(default=False, null=True)),
                ('comm_counter', models.IntegerField(default=0)),
                ('obs_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='ObservationComment',
            new_name='Comment',
        ),
        migrations.DeleteModel(
            name='ObservationNormal',
        ),
        migrations.AlterField(
            model_name='comment',
            name='observation_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.observation'),
        ),
    ]
