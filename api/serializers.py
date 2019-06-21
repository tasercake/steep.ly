from rest_framework import serializers
from .models import Terrain


class TerrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terrain
        fields = ('pk', 'height')


class SimpleTerrainRequestSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        terrain = Terrain()
        # TODO: Do stuff with terrain
        terrain.save()
        return terrain
