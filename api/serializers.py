from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Terrain
from .terrain_generator import TerrainGenerator


class TerrainSerializer(serializers.ModelSerializer):
    height = serializers.ImageField()

    class Meta:
        model = Terrain
        fields = ('slug', 'height')


class SimpleTerrainRequestSerializer(serializers.Serializer):
    seed = serializers.IntegerField(default=0)
    scale = serializers.FloatField(default=1)
    detail = serializers.IntegerField(default=2)

    def update(self, terrain, validated_data):
        raise NotImplementedError()

    def create(self, options):
        terrain = Terrain()
        images = TerrainGenerator(options).generate_images()
        for field_name, image in images.items():
            field = getattr(terrain, field_name)
            blob = BytesIO()
            image.save(blob, 'JPEG', quality=50)
            field.save(f'{terrain.slug}/{terrain.slug}_{field_name}.jpg', ContentFile(blob.getvalue()), save=False)
        terrain.save()
        return terrain
