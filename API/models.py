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

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    x_coords = models.FloatField(default=0)
    y_coords = models.FloatField(default=0)
    name = models.CharField(max_length=150)
    time = models.DateTimeField(default=datetime.now(tz=None))
    photo = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


# Observation data - Simple
class ObservationSimple(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    x_coords = models.FloatField(default=0)
    y_coords = models.FloatField(default=0)
    size = models.CharField(max_length=70)
    # family = models.CharField(max_length=70) ???
    # color = models.CharField(max_length=70) ???
    description = models.CharField(max_length=300)
    time = models.DateTimeField(default=datetime.now(tz=None))
    photo = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name
