from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from rest_framework import serializers
from .models import Terrain


class TerrainSerializer(serializers.ModelSerializer):
    height = serializers.ImageField()

    class Meta:
        model = Terrain
        fields = ('pk', 'slug', 'height')


class SimpleTerrainRequestSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        terrain = Terrain()
        height = Image.new('RGB', (100, 100))
        images = {'height': height}
        self._save_images(images, terrain)
        terrain.save()
        return terrain

    def _save_images(self, images: dict, instance):
        for field_name, image in images.items():
            field = getattr(instance, field_name)
            blob = BytesIO()
            image.save(blob, 'JPEG', quality=50)
            field.save(f'{instance.slug}/{instance.slug}_{field_name}.jpg', ContentFile(blob.getvalue()), save=False)
