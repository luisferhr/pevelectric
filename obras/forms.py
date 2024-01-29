from django import forms
from .models import Obra  # Importa el modelo Obra

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['numero_obra', 'descripcion', 'lugar', 'material', 'apoyo_data']
