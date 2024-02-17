from django import forms
from usuario.models import Emergencia
from django.utils import timezone

class CrearEmergenciaForm(forms.ModelForm):
    class Meta:
        model = Emergencia
        fields = ['descripcion', 'lugar', 'fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CrearEmergenciaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].initial = timezone.localtime().date()

class ModificarEmergenciaForm(forms.ModelForm):
    numero_obra = forms.CharField(required=False, label="Número de Obra")

    class Meta:
        model = Emergencia
        fields = ['id_emergencia', 'descripcion', 'lugar', 'fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }