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
from .views import *
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('user/login/', LoginAPI.as_view(), name='login'),
    #path('user/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/user/', UserAPI.as_view(), name='user'),
    # path('add_observation/')
]
