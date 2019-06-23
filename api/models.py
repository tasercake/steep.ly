from django.db import models
from django.utils.crypto import get_random_string


def get_unique_slug():
    return get_random_string(6).upper()


class Terrain(models.Model):
    slug = models.CharField(max_length=8, unique=True, null=False, default=get_unique_slug)
    height = models.ImageField(null=False)
    options = models.FileField(null=True)
