from django.contrib import admin
from .models import Terrain


# Register your models here.
@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    pass
