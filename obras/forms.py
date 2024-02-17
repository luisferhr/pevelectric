from django.utils import timezone
from django import forms
from django.forms.widgets import DateInput
from obras.admin import RetiroMaterialInline
from usuario.models import Obra
from usuario.models import TipoMaterial, RetiroMaterial, DevolucionMaterial, Emergencia

class CrearObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['id_obra', 'descripcion', 'lugar', 'fecha_inicio', 'tipo_obra']  # Incluye 'fecha_inicio'
        widgets = {
            'tipo_obra': forms.TextInput(attrs={'placeholder': 'Opcional'}),
            'fecha_inicio': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CrearObraForm, self).__init__(*args, **kwargs)
        self.fields['tipo_obra'].required = False
        self.fields['fecha_inicio'].initial = timezone.localtime().date()

class RetiroForm(forms.Form):
    def __init__(self, obra=None, *args, **kwargs):
        super(RetiroForm, self).__init__(*args, **kwargs)
        if obra:
            self.fields.clear()
            for tipo_material in TipoMaterial.objects.all():
                if tipo_material.nombre.lower() not in ['ferreteria', 'ferretería']:
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
                else:
                    retiro_material, _ = RetiroMaterial.objects.get_or_create(
                        obra=obra,
                        tipo_material=tipo_material,
                        defaults={'cantidad_retirada': 0}
                    )
                    si_retira = True if retiro_material.cantidad_retirada > 0 else False
                    self.fields['si_ferreteria'] = forms.BooleanField(initial=si_retira, required=False)

class DevolucionForm(forms.Form):
    def __init__(self, obra=None, *args, **kwargs):
        super(DevolucionForm, self).__init__(*args, **kwargs)
        if obra:
            self.fields.clear()
            for tipo_material in TipoMaterial.objects.all():
                if tipo_material.nombre.lower() not in ['ferreteria', 'ferretería']:
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
                else:
                    devolucion_material, _ = DevolucionMaterial.objects.get_or_create(
                        obra=obra,
                        tipo_material=tipo_material,
                        defaults={'cantidad_devuelta': 0}
                    )
                    si_devuelve = True if devolucion_material.cantidad_devuelta > 0 else False
                    self.fields['si_ferreteria'] = forms.BooleanField(initial=si_devuelve, required=False)

class ModificarObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['descripcion', 'lugar', 'si_finalizo', 'tipo_obra']  # Especifica los campos a incluir
        widgets = {
            'tipo_obra': forms.TextInput(attrs={'placeholder': 'Opcional'}),
            'si_finalizo': forms.CheckboxInput(),
        }
