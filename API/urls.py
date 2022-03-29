"""BP_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .models import *
from .views import ViewUsers, RegisterUser, LoginUser, CreateNewNormalObservation, WhoAmI, CreateNewSimpleObservation, \
    GetRecentNormalObservations
from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('users/', ViewUsers.as_view()),
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('observation/normal/', CreateNewNormalObservation.as_view()),
    path('observation/simple/', CreateNewSimpleObservation.as_view()),
    path('whoami/', WhoAmI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('observation/recent/', GetRecentNormalObservations.as_view()),
    # path('register/', Register.as_view(), name='register'), # register new user
    # path('user/login/', LoginAPI.as_view(), name='login'), # login user
    # #path('user/logout/', knox_views.LogoutView.as_view(), name='logout'), # logout user
    # path('api/user/', UserAPI.as_view(), name='user'), # get info about user?
    # path('add_observation/' ObservationNormal)
]
