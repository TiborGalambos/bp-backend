from rest_framework import serializers
from django.contrib.auth.models import User



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')



# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])

        return user

# Adding Observations
class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'


# User Serializer
# class UserSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = User
#     fields = ('id', 'username', 'email')