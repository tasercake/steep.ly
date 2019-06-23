import json
from io import BytesIO, StringIO
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
    MAX_PREVIEW_SIZE = 1024
    MAX_SIZE = 8192

    preview_size = serializers.IntegerField(default=512)
    size = serializers.IntegerField(default=2048)
    seed = serializers.IntegerField(default=0)
    scale = serializers.FloatField(default=1)
    depth = serializers.IntegerField(default=4)

    def validate(self, options):
        return options

    def update(self, terrain, validated_data):
        raise NotImplementedError()

    def create(self, options):
        terrain = Terrain()
        generator = TerrainGenerator(options)
        images = generator.generate_images()
        for field_name, image in images.items():
            field = getattr(terrain, field_name)
            blob = BytesIO()
            image.save(blob, 'JPEG', quality=50)
            field.save(f'{terrain.slug}/{terrain.slug}_{field_name}.jpg', ContentFile(blob.getvalue()), save=False)
        options = StringIO(json.dumps(generator.options))
        terrain.options.save(f'{terrain.slug}/{terrain.slug}_options.json', ContentFile(options.getvalue()), save=False)
        terrain.save()
        return terrain
