from django.contrib import admin
from usuario.models import Emergencia

class EmergenciaAdmin(admin.ModelAdmin):
    list_display = ('id_emergencia', 'descripcion', 'lugar', 'fecha_inicio')  # Campos que quieres mostrar en la lista
    search_fields = ['descripcion', 'lugar']  # Campos por los cuales se puede buscar
    list_filter = ('fecha_inicio',)  # Filtros disponibles en la barra lateral

# Registrar el modelo y su configuración en el admin
admin.site.register(Emergencia, EmergenciaAdmin)