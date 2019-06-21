from django import forms
from .models import Terrain


class TerrainForm(forms.ModelForm):
    class Meta:
        model = Terrain
        fields = ('height',)
