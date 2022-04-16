from django.core.paginator import Paginator

from API.serializers import *
from rest_framework import generics, permissions
from rest_framework.response import Response


def update_global_stats(observation_data):
    exact_bird = BirdCounter.objects.filter(bird_name__contains=observation_data['bird_name'])
    exact_bird_first = exact_bird.first()
    print(exact_bird)
    if exact_bird.count() == 0:
        print("none")
        new_data = BirdCounter(bird_name=observation_data['bird_name'], bird_count=observation_data['bird_count'])
        new_data.save()
    else:
        print("something")
        new_count = int(getattr(exact_bird_first, 'bird_count')) + int(observation_data['bird_count'])
        exact_bird.update(bird_count=new_count)


def update_personal_stats(observation_data, user_id):
    exact_stat = PersonalStats.objects.filter(author_id__exact=observation_data['author_id'])
    exact_stat_first = exact_stat.first()

    if exact_stat.count() == 0:
        print("none")
        new_data = PersonalStats(author_id=user_id, obs_count=observation_data['bird_count'])
        new_data.save()
    else:
        print("something")
        new_count = int(getattr(exact_stat_first, 'obs_count')) + int(observation_data['bird_count'])
        exact_stat.update(obs_count=new_count)


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

        print(type(observation_data))

        observation_data['author_id'] = user.id
        observation_data['obs_is_simple'] = False
        observation_data['bird_photo'] = photo

        serializer = self.get_serializer(data=observation_data)
        serializer.is_valid(raise_exception=True)

        item = serializer.save()

        update_global_stats(observation_data)
        update_personal_stats(observation_data, user)
        request.FILES['bird_photo'].close()

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

        observation_data['author_id'] = user.id
        observation_data['obs_author_name'] = user.username
        observation_data['obs_is_confirmed'] = False
        observation_data['bird_photo'] = photo

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

        observations = Observation.objects.all().filter(obs_is_confirmed=True).order_by('-id')[:10]

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


class UpdateUnconfirmedObservation(generics.UpdateAPIView):

    permission_classes = [permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):

        obs_number = self.kwargs['obs_number']

        observation_data = request.POST.copy()

        observation = Observation.objects.filter(pk=obs_number).first()

        observation.bird_name = observation_data['bird_name']
        observation.obs_is_simple = False
        observation.obs_is_confirmed = True

        observation.save()

        return Response({"updated": True}, status=200)

