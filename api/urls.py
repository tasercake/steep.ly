from django.urls import include, path
from . import views

app_name = 'api'

urlpatterns = [
    path("terrain/", views.GenerateTerrain.as_view(), name='generate_terrain'),
    path("terrain/<key>/", views.GetTerrain.as_view(), name='get_terrain'),
]
