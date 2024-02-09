from django.contrib import admin
from .models import Obra, TipoMaterial, MaterialObra

# Opcional: Personalizar la visualización de Obra en el admin
class MaterialObraInline(admin.TabularInline):
    model = MaterialObra
    extra = 1  # Número de formas extra para materiales a mostrar

class ObraAdmin(admin.ModelAdmin):
    inlines = [MaterialObraInline]
    list_display = ('id_obra', 'descripcion', 'lugar', 'si_emergencia', 'si_retira', 'si_devuelve')  # Campos a mostrar en la lista
    search_fields = ['id_obra', 'descripcion', 'lugar']  # Campos por los que se puede buscar

# Registrar los modelos y sus configuraciones personalizadas si las hay
admin.site.register(Obra, ObraAdmin)
admin.site.register(TipoMaterial)  # TipoMaterial se registra sin personalizaciones específicas
