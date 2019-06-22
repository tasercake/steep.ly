from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Terrain
from .serializers import TerrainSerializer, SimpleTerrainRequestSerializer


def serialize_terrain(terrain, request=None):
    context = {'request': request} if request else None
    serializer = TerrainSerializer(terrain, context=context)
    return serializer.data


class GetTerrain(APIView):
    def get(self, request, key):
        try:
            terrain = Terrain.objects.get(slug=key)
        except Terrain.DoesNotExist as e:  # Allow access by PK in development
            if settings.DEBUG:
                terrain = Terrain.objects.get(pk=key)
            else:
                raise e
        return Response(serialize_terrain(terrain, request=request), status=status.HTTP_200_OK)


class GenerateTerrain(APIView):
    def post(self, request):
        serializer = SimpleTerrainRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        terrain = serializer.save()
        return Response(terrain.slug, status=status.HTTP_201_CREATED)


class TerrainViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Terrain.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SimpleTerrainRequestSerializer
        elif self.request.method == 'GET':
            return TerrainSerializer

    def create(self, request, *args, **kwargs):
        serializer = SimpleTerrainRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        terrain = serializer.save()
        return Response({'pk': terrain.pk}, status=status.HTTP_201_CREATED)
