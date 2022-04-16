from django.db.models import Sum
from rest_framework import generics, permissions
from rest_framework.response import Response

from API.models import BirdCounter, PersonalStats
from API.serializers import BirdCounterSerializer, PersonalStatsSerializer


class GetGlobalStatisticsMainNumbers(generics.RetrieveAPIView):
    serializer_class = BirdCounterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        stats = BirdCounter.objects.aggregate(Sum('bird_count'))

        return Response({"sum": stats})


class GetGlobalSumOfBirds(generics.RetrieveAPIView):
    serializer_class = BirdCounterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        stats = BirdCounter.objects.order_by('-bird_count')
        serializer = BirdCounterSerializer(stats, many=True)

        return Response({"birds": serializer.data})


class GetPersonalSumOfBirds(generics.RetrieveAPIView):
    serializer_class = PersonalStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        stats = PersonalStats.objects.filter(author_id__exact=request.user.id).first().obs_count

        return Response({"sum": {"bird_count__sum": stats}})