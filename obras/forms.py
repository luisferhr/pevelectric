from django import forms
from django.forms.widgets import DateInput
from usuario.models import Obra
from usuario.models import TipoMaterial, MaterialObra

class ObraSimpleForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['id_obra', 'descripcion', 'lugar', 'si_emergencia', 'si_retira', 'si_devuelve', 'fecha_inicio', 'fecha_termino', 'tipo_obra']
        widgets = {
            'si_emergencia': forms.CheckboxInput(),
            'si_retira': forms.CheckboxInput(),
            'si_devuelve': forms.CheckboxInput(),
            'fecha_inicio': DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'fecha_termino': DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}),
            'tipo_obra': forms.TextInput(attrs={'placeholder': 'Opcional'}),
        }

    def __init__(self, *args, **kwargs):
        super(ObraSimpleForm, self).__init__(*args, **kwargs)
        # Establecer los valores iniciales para los campos booleanos
        self.initial['si_emergencia'] = False
        self.initial['si_retira'] = False
        self.initial['si_devuelve'] = False

class RetiroForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RetiroForm, self).__init__(*args, **kwargs)
        for tipo_material in TipoMaterial.objects.all():
            field_name = f"material_{tipo_material.id}"
            self.fields[field_name] = forms.IntegerField(label=tipo_material.nombre, required=False, min_value=0)