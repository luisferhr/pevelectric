from django import forms
from django.forms.widgets import DateInput
from usuario.models import Obra
from usuario.models import TipoMaterial, RetiroMaterial, DevolucionMaterial

class ObraSimpleForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['id_obra', 'descripcion', 'lugar', 'si_emergencia', 'fecha_inicio', 'fecha_termino', 'tipo_obra']
        widgets = {
            'si_emergencia': forms.CheckboxInput(),
            'fecha_inicio': DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'fecha_termino': DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'tipo_obra': forms.TextInput(attrs={'placeholder': 'Opcional'}),
        }

    def __init__(self, *args, **kwargs):
        super(ObraSimpleForm, self).__init__(*args, **kwargs)
        self.initial['si_emergencia'] = False

class RetiroForm(forms.Form):
    def __init__(self, obra=None, *args, **kwargs):
        super(RetiroForm, self).__init__(*args, **kwargs)
        if obra:
            self.fields.clear()
            for tipo_material in TipoMaterial.objects.all():
                retiro_material, _ = RetiroMaterial.objects.get_or_create(
                    obra=obra,
                    tipo_material=tipo_material,
                    defaults={'cantidad_retirada': 0}
                )
                self.fields[f"retiro_{tipo_material.idMaterial}"] = forms.IntegerField(
                    label=tipo_material.nombre,
                    initial=retiro_material.cantidad_retirada,
                    required=False,
                    min_value=0
                )

class DevolucionForm(forms.Form):
    def __init__(self, obra=None, *args, **kwargs):
        super(DevolucionForm, self).__init__(*args, **kwargs)
        if obra:
            self.fields.clear()
            for tipo_material in TipoMaterial.objects.all():
                devolucion_material, _ = DevolucionMaterial.objects.get_or_create(
                    obra=obra,
                    tipo_material=tipo_material,
                    defaults={'cantidad_devuelta': 0}
                )
                self.fields[f"devolucion_{tipo_material.idMaterial}"] = forms.IntegerField(
                    label=tipo_material.nombre,
                    initial=devolucion_material.cantidad_devuelta,
                    required=False,
                    min_value=0
                )

class ObraModificaForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['id_obra', 'descripcion', 'lugar', 'si_emergencia', 'fecha_inicio', 'fecha_termino', 'tipo_obra', 'si_finalizo']
        widgets = {
            'si_emergencia': forms.CheckboxInput(),
            'fecha_inicio': DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'fecha_termino': DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'tipo_obra': forms.TextInput(attrs={'placeholder': 'Opcional'}),
            'si_termino': forms.CheckboxInput(),
            # Agrega un widget si es necesario para 'si_finalizo'
        }
