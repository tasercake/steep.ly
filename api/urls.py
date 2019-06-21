from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'
# router = DefaultRouter()
# router.register("terrain", views.TerrainViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path("", views.GenerateTerrain.as_view(), name='generate_terrain'),
    path("<int:pk>/", views.GetTerrain.as_view(), name='get_terrain'),
]
