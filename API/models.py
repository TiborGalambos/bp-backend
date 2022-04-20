from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
import datetime
from django.contrib.auth import login
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.views import APIView



# Observation data
class Observation(models.Model):
    author_id = models.ForeignKey(User, related_name='obs_author', on_delete=models.CASCADE)

    obs_x_coords = models.FloatField(default=0)
    obs_y_coords = models.FloatField(default=0)

    obs_place = models.CharField(max_length=200, default="Nowhere")

    obs_is_confirmed = models.BooleanField(null=True, default=False)

    bird_name = models.CharField(max_length=150, default="Neurčený")
    bird_count = models.IntegerField(default=1)
    obs_time = models.DateField(default=datetime.date.today())
    bird_photo = models.ImageField(null=True, blank=True, upload_to="images/")
    bird_recording = models.FileField(null=True, blank=True, upload_to="recording/", default=None)

    bird_size = models.CharField(max_length=150, default=None, null=True)
    bird_color = models.CharField(max_length=150, default=None, null=True)
    bird_beak = models.CharField(max_length=150, default=None, null=True)


    obs_description = models.CharField(max_length=300, default=None, null=True)

    obs_is_simple = models.BooleanField(null=True, default=False)

    def __int__(self):
        return self.bird_name


class Comment(models.Model):
    author_id = models.ForeignKey(User, related_name='com_author', on_delete=models.CASCADE)
    observation_id = models.ForeignKey(Observation, related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, default=None, null=True)

    def __str__(self):
        return self.comment


# model for personal observation count
class PersonalStats(models.Model):
    author_id = models.ForeignKey(User, related_name='stat_author', on_delete=models.CASCADE)
    obs_count = models.IntegerField(default=0)

    def __str__(self):
        return self.obs_count


# model for count of all birds
class BirdCounter(models.Model):
    bird_name = models.CharField(max_length=500, default=None, null=True)
    bird_count = models.IntegerField(default=0)

    def __str__(self):
        return self.bird_name

