from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from API.serializers import *
from django.contrib.auth import login
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.views import APIView

# Observation data
class Observations(models.Model):
    serializer_class = ObservationSerializer

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    x_coords = models.FloatField(default=0)
    y_coords = models.FloatField(default=0)
    size = models.CharField(max_length=70)
    color = models.CharField(max_length=70)
    description = models.CharField(max_length=300)
    time = models.DateTimeField(default=datetime.now(tz=None))
    photo = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


# User Registration data
class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)    # serializer variable <- Register Serializer data
        serializer.is_valid(raise_exception=True)    # check if serializes with Register Serializer data is valid, if not, raise exception
        user = serializer.save()    # save

        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]})


# Login User
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return super(LoginAPI, self).post(request, format=None)

# Get currently logged in user
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user