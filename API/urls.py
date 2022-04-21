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
from .views import CreateNewNormalObservation, CreateNewSimpleObservation, \
    GetRecentConfirmedObservationsWithComments, GetAllPersonalObservationsPagination, CreateComment, \
    GetAllConfirmedObsWithCommentsPagination, GetAllUnconfirmedObservationsWithComments, UpdateUnconfirmedObservation, \
    GetObsBySpecies, GetSpeciesByYear, DeleteMyObservation
from .stats_views.stats_views import GetGlobalStatisticsMainNumbers, GetGlobalSumOfBirds, GetPersonalSumOfBirds
from .user_views.user_views import ViewUsers, RegisterUser, LoginUser, WhoAmI, AmIAdmin
from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('users/', ViewUsers.as_view()),
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('whoami/', WhoAmI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('amiadmin/', AmIAdmin.as_view()),

    path('observation/normal/', CreateNewNormalObservation.as_view()),
    path('observation/simple/', CreateNewSimpleObservation.as_view()),


    path('observation/recent/', GetRecentConfirmedObservationsWithComments.as_view()),
    path('observation/unconfirmed/<int:page_number>', GetAllUnconfirmedObservationsWithComments.as_view(), name='page_number'),
    path('observation/unconfirmed/update/<int:obs_number>', UpdateUnconfirmedObservation.as_view(), name='obs_number'),
    path('observation/unconfirmed/', GetAllUnconfirmedObservationsWithComments.as_view()),



    path('observation/user/<int:page_number>', GetAllPersonalObservationsPagination.as_view(), name='page_number'),
    path('observation/user/', GetAllPersonalObservationsPagination.as_view()),


    path('observation/newcomment/', CreateComment.as_view()),
    path('observation/delete/', DeleteMyObservation.as_view()),

    path('observation/comments/<int:page_number>', GetAllConfirmedObsWithCommentsPagination.as_view(), name='page_number'),
    path('observation/comments/', GetAllConfirmedObsWithCommentsPagination.as_view()),


    path('stats/sum/', GetGlobalStatisticsMainNumbers.as_view()),
    path('stats/birds/', GetGlobalSumOfBirds.as_view()),
    path('stats/sum/personal/', GetPersonalSumOfBirds.as_view()),


    path('observation/species/locations/', GetObsBySpecies.as_view()),
    path('observation/species/occurrence/', GetSpeciesByYear.as_view())

]
