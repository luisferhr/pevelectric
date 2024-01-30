from django import forms
from usuario.models import Obra, Material
class ObraSimpleForm(forms.Form):
    id_obra = forms.CharField()
    descripcion = forms.CharField()
    lugar = forms.CharField()
    fk_material = forms.CharField() 
    emergencia = forms.BooleanField(required=False, initial=False)
    def __init__(self, *args, **kwargs):
        super(ObraSimpleForm, self).__init__(*args, **kwargs)
        self.initial['emergencia'] = False