from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from rest_framework import serializers

# User Serializer
from API.models import ObservationNormal, ObservationSimple


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("wrong login")
        return user


# Adding Normal Observations
class NormalObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationNormal
        fields = '__all__'


# Adding Simple Observations
class SimpleObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationSimple
        fields = '__all__'


