import knox.knox
from django.shortcuts import render
from django.http import HttpResponse
from knox.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from API.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib import auth
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from knox.models import AuthToken


class ViewUsers(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        users_to_show = User.objects.all()

        serializer = UserSerializer(users_to_show, many=True)
        return Response(serializer.data)


class RegisterUser(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(username=request.POST['username'])
        user.set_password(request.POST['password'])

        user.save()
        _, token = AuthToken.objects.create(user)

        return Response(
            {"user": user.username,
             "token": token})


class LoginUser(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        _, token = AuthToken.objects.create(user)

        return Response(
            {
                "user": user.username,
                "token": token
            }
        )


class WhoAmI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        print(request.user.is_superuser)
        return Response({'name': user.username})


class CreateNewNormalObservation(generics.CreateAPIView):
    serializer_class = NormalObservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        observation_data = request.POST.copy()
        try:
            photo = request.FILES['photo']
        except:
            photo = None

        observation_data['author'] = user.id
        observation_data['author_name'] = user.username
        observation_data['photo'] = photo

        serializer = self.get_serializer(data=observation_data)
        serializer.is_valid(raise_exception=True)

        item = serializer.save()

        return Response(serializer.data)
