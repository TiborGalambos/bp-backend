from django.contrib.auth.models import User
from knox.models import AuthToken
from knox.serializers import UserSerializer
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from API.serializers import UserSerializer, RegisterSerializer


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


class AmIAdmin(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        user = request.user

        isAdmin = user.is_staff

        return Response({'is_admin': isAdmin})
