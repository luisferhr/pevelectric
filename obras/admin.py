from django.contrib import admin
from usuario.models import Obra, TipoMaterial, RetiroMaterial, DevolucionMaterial

# Personalizar la visualización de RetiroMaterial en el admin
class RetiroMaterialInline(admin.TabularInline):
    model = RetiroMaterial
    extra = 0  # No se añaden filas extra automáticamente

# Personalizar la visualización de DevolucionMaterial en el admin
class DevolucionMaterialInline(admin.TabularInline):
    model = DevolucionMaterial
    extra = 0  # No se añaden filas extra automáticamente

class ObraAdmin(admin.ModelAdmin):
    inlines = [RetiroMaterialInline, DevolucionMaterialInline]
    list_display = ('id_obra', 'descripcion', 'lugar', 'si_emergencia', 'fecha_inicio', 'fecha_termino', 'si_finalizo', 'tipo_obra')
    search_fields = ['id_obra', 'descripcion', 'lugar']
    list_filter = ('si_emergencia', 'fecha_inicio', 'fecha_termino', 'si_finalizo', 'tipo_obra')

class TipoMaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'stock')
    search_fields = ['nombre', 'descripcion']

# Registrar los modelos y sus configuraciones personalizadas
admin.site.register(Obra, ObraAdmin)
admin.site.register(TipoMaterial, TipoMaterialAdmin)