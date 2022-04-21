import json
import time

from django.core.paginator import Paginator

from API.serializers import *
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Sum
import geopy.distance


def update_global_stats(bird_name, bird_count):
    exact_bird = BirdCounter.objects.filter(bird_name__contains=bird_name)
    exact_bird_first = exact_bird.first()
    print(exact_bird)
    if exact_bird.count() == 0:
        print("none")
        new_data = BirdCounter(bird_name=bird_name, bird_count=bird_count)
        new_data.save()
    else:
        print("something")
        new_count = int(getattr(exact_bird_first, 'bird_count')) + int(bird_count)
        exact_bird.update(bird_count=new_count)


def update_personal_stats(bird_count, user):
    exact_stat = PersonalStats.objects.filter(author_id__exact=user.id)
    exact_stat_first = exact_stat.first()

    if exact_stat.count() == 0:
        print("none")
        new_data = PersonalStats(author_id=user, obs_count=bird_count)
        new_data.save()
    else:
        print("something")
        new_count = int(getattr(exact_stat_first, 'obs_count')) + int(bird_count)
        exact_stat.update(obs_count=new_count)


def auto_confirm(observation_data):
    exact_observations = Observation.objects.filter(bird_name__contains=observation_data['bird_name'],
                                                    obs_is_confirmed=True).all()

    new_location_coords = (float(observation_data['obs_y_coords']), float(observation_data['obs_x_coords']))
    required_bird_count: int = int(observation_data['bird_count']) * 3

    print("required: " + str(required_bird_count))

    actual_bird_count: int = 0

    for i in exact_observations:

        location = (float(i.obs_y_coords), float(i.obs_x_coords))

        distance = geopy.distance.geodesic(new_location_coords, location).km

        print("distance: " + str(distance))

        if distance < 30:
            actual_bird_count += i.bird_count
            print("update actual: " + str(actual_bird_count))

            if int(actual_bird_count) >= int(required_bird_count):
                print("returning true " + str(actual_bird_count))
                return True

    print("returning false " + str(actual_bird_count))
    return False


class CreateNewNormalObservation(generics.CreateAPIView):
    serializer_class = ObservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        observation_data = request.POST.copy()
        try:
            photo = request.FILES['bird_photo']
        except:
            photo = None

        try:
            recording = request.FILES['bird_recording']
        except:
            recording = None

        observation_data['author_id'] = user.id
        observation_data['obs_is_simple'] = False
        observation_data['bird_photo'] = photo
        observation_data['bird_recording'] = recording

        observation_data['obs_is_confirmed'] = False

        if auto_confirm(observation_data):
            observation_data['obs_is_confirmed'] = True
            update_global_stats(str(observation_data['bird_name']), int(observation_data['bird_count']))
            update_personal_stats(int(observation_data['bird_count']), user)

        serializer = self.get_serializer(data=observation_data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()

        # request.FILES['bird_photo'].close()

        return Response(serializer.data)


class CreateNewSimpleObservation(generics.CreateAPIView):
    serializer_class = ObservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        observation_data = request.POST.copy()
        try:
            photo = request.FILES['bird_photo']
        except:
            photo = None

        try:
            recording = request.FILES['bird_recording']
        except:
            recording = None

        observation_data['author_id'] = user.id
        observation_data['obs_author_name'] = user.username
        observation_data['obs_is_confirmed'] = False
        observation_data['bird_photo'] = photo
        observation_data['bird_recording'] = recording

        observation_data['obs_is_simple'] = True

        serializer = self.get_serializer(data=observation_data)
        serializer.is_valid(raise_exception=True)

        item = serializer.save()

        return Response(serializer.data)


class CreateComment(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        observation_data = request.POST.copy()

        observation_data['author_id'] = user.id

        serializer = self.get_serializer(data=observation_data)
        serializer.is_valid(raise_exception=True)

        item = serializer.save()

        return Response(serializer.data)


# For Home page
class GetRecentConfirmedObservationsWithComments(generics.RetrieveAPIView):
    serializer_class = ObservationAndCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        try:
            page_number = self.kwargs['page_number']
        except:
            page_number = 1

        observations = Observation.objects.all().filter(obs_is_confirmed=True, obs_is_simple=False).order_by('-id')[:10]

        p = Paginator(observations, 10)

        obs_list = p.page(page_number)

        serializer = ObservationAndCommentSerializer(obs_list, many=True)

        return Response({'obs': serializer.data,
                         'paginator': {
                             'total_pages': p.num_pages,
                             'current_page': page_number,
                             'has_next': obs_list.has_next(),
                             'has_prev': obs_list.has_previous()
                         }})


# For specialist
class GetAllUnconfirmedObservationsWithComments(generics.RetrieveAPIView):
    serializer_class = ObservationAndCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        try:
            page_number = self.kwargs['page_number']
        except:
            page_number = 1

        observations = Observation.objects.filter(obs_is_confirmed=False).order_by('-id')

        p = Paginator(observations, 10)

        obs_list = p.page(page_number)

        serializer = ObservationAndCommentSerializer(obs_list, many=True)

        return Response({'obs': serializer.data,
                         'paginator': {
                             'total_pages': p.num_pages,
                             'current_page': page_number,
                             'has_next': obs_list.has_next(),
                             'has_prev': obs_list.has_previous()
                         }})


# For Personal collection
class GetAllPersonalObservationsPagination(generics.RetrieveAPIView):
    serializer_class = ObservationAndCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            page_number = self.kwargs['page_number']
        except:
            page_number = 1

        observations = Observation.objects.filter(author_id__exact=user.id).order_by('-id')

        p = Paginator(observations, 10)

        obs_list = p.page(page_number)

        serializer = ObservationAndCommentSerializer(obs_list, many=True)

        return Response({'obs': serializer.data,
                         'paginator': {
                             'total_pages': p.num_pages,
                             'current_page': page_number,
                             'has_next': obs_list.has_next(),
                             'has_prev': obs_list.has_previous()
                         }})


# For Search Page
class GetAllConfirmedObsWithCommentsPagination(generics.RetrieveAPIView):
    serializer_class = ObservationAndCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        try:
            page_number = self.kwargs['page_number']
        except:
            page_number = 1

        observations = Observation.objects.all().order_by('-id')

        p = Paginator(observations, 10)

        obs_list = p.page(page_number)

        serializer = ObservationAndCommentSerializer(obs_list, many=True)

        return Response({'obs': serializer.data,
                         'paginator': {
                             'total_pages': p.num_pages,
                             'current_page': page_number,
                             'has_next': obs_list.has_next(),
                             'has_prev': obs_list.has_previous()
                         }})


class DeleteMyObservation(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        body = request.POST.copy
        obs_number = request.POST['obs_number']

        observation = Observation.objects.filter(pk=obs_number).first()
        print(request.user)
        # print(observation.author_id)

        if observation is None:
            return Response({"deleted": False}, status=404)

        if request.user == observation.author_id:
            observation.delete()
            return Response({"deleted": True}, status=201)

        return Response({"deleted": False}, status=401)


class UpdateUnconfirmedObservation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):
        obs_number = self.kwargs['obs_number']

        observation_data = request.POST.copy()

        observation = Observation.objects.filter(pk=obs_number).first()

        observation.bird_name = observation_data['bird_name']
        observation.obs_is_simple = False
        observation.obs_is_confirmed = True

        observation.save()

        user_obj = observation.author_id

        update_global_stats(str(observation_data['bird_name']), int(observation.bird_count))

        update_personal_stats(int(observation.bird_count), user_obj)

        return Response({"updated": True}, status=200)

    def delete(self, request, *args, **kwargs):
        obs_number = self.kwargs['obs_number']
        observation = Observation.objects.filter(pk=obs_number).first().delete()

        return Response({"deleted": True}, status=201)


class GetObsBySpecies(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ObservationAndCommentSerializer

    def put(self, request, *args, **kwargs):
        observation_data = request.POST.copy()
        species = observation_data['bird_name']

        observations = Observation.objects.all().filter(bird_name__contains=species)
        serializer = ObservationSerializer(observations, many=True)

        return Response({"obs": serializer.data})


class GetSpeciesByYear(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        observation_data = request.POST.copy()
        species = observation_data['bird_name']
        year = observation_data['year']
        observations = Observation.objects.filter(bird_name__contains=species, obs_time__year=year).values()

        jan = observations.filter(obs_time__month=1).aggregate(total=Sum('bird_count'))['total']
        feb = observations.filter(obs_time__month=2).aggregate(total=Sum('bird_count'))['total']
        mar = observations.filter(obs_time__month=3).aggregate(total=Sum('bird_count'))['total']
        apr = observations.filter(obs_time__month=4).aggregate(total=Sum('bird_count'))['total']
        maj = observations.filter(obs_time__month=5).aggregate(total=Sum('bird_count'))['total']
        jun = observations.filter(obs_time__month=6).aggregate(total=Sum('bird_count'))['total']
        jul = observations.filter(obs_time__month=7).aggregate(total=Sum('bird_count'))['total']
        aug = observations.filter(obs_time__month=8).aggregate(total=Sum('bird_count'))['total']
        sep = observations.filter(obs_time__month=9).aggregate(total=Sum('bird_count'))['total']
        octo = observations.filter(obs_time__month=10).aggregate(total=Sum('bird_count'))['total']
        nov = observations.filter(obs_time__month=11).aggregate(total=Sum('bird_count'))['total']
        dec = observations.filter(obs_time__month=12).aggregate(total=Sum('bird_count'))['total']

        if jan is None:
            jan = 0
        if feb is None:
            feb = 0
        if mar is None:
            mar = 0
        if apr is None:
            apr = 0
        if maj is None:
            maj = 0
        if jun is None:
            jun = 0
        if jul is None:
            jul = 0
        if aug is None:
            aug = 0
        if sep is None:
            sep = 0
        if octo is None:
            octo = 0
        if nov is None:
            nov = 0
        if dec is None:
            dec = 0

        # serializer = ObservationSerializer(observations, many=True)

        return Response({"year": {
            "jan": int(jan),
            "feb": int(feb),
            "mar": int(mar),
            "apr": int(apr),
            "maj": int(maj),
            "jun": int(jun),
            "jul": int(jul),
            "aug": int(aug),
            "sep": int(sep),
            "oct": int(octo),
            "nov": int(nov),
            "dec": int(dec),
        }})
