from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from knox.serializers import UserSerializer
from rest_framework import serializers

# User Serializer
from rest_framework.relations import *

from API.models import Observation, Comment, PersonalStats, BirdCounter


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
class ObservationSerializer(serializers.ModelSerializer):
    def get_username(self, obj):
        return obj.author_id.username

    obs_author = serializers.SerializerMethodField("get_username")

    class Meta:
        model = Observation
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    def get_username(self, obj):
        return obj.author_id.username

    com_author = serializers.SerializerMethodField("get_username")

    class Meta:
        model = Comment
        fields = '__all__'


class ObservationAndCommentSerializer(serializers.ModelSerializer):
    def get_username(self, obj):
        return obj.author_id.username

    obs_author = serializers.SerializerMethodField("get_username")

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Observation
        fields = '__all__'


class PersonalStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalStats
        fields = '__all__'


class BirdCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirdCounter
        fields = '__all__'
