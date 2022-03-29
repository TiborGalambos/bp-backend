from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from django.contrib.auth import login
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.views import APIView


# Observation data - Normal
class ObservationNormal(models.Model):

    obs_author = models.ForeignKey(User, on_delete=models.CASCADE)
    obs_author_name = models.CharField(max_length=150, default="username")
    obs_x_coords = models.FloatField(default=0)
    obs_y_coords = models.FloatField(default=0)
    bird_name = models.CharField(max_length=150)
    bird_count = models.IntegerField(default=1)
    obs_time = models.DateTimeField(default=datetime.now(tz=None))
    bird_photo = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


# Observation data - Simple
class ObservationSimple(models.Model):

    obs_author = models.ForeignKey(User, on_delete=models.CASCADE)
    obs_author_name = models.CharField(max_length=150, default="username")
    obs_x_coords = models.FloatField(default=0)
    obs_y_coords = models.FloatField(default=0)
    bird_size = models.CharField(max_length=70)
    # bird_family = models.CharField(max_length=70) ???
    # bird_color = models.CharField(max_length=70) ???
    bird_count = models.IntegerField(default=1)
    obs_description = models.CharField(max_length=300, default=None, null=True,)
    obs_time = models.DateTimeField(default=datetime.now(tz=None))
    bird_photo = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name
