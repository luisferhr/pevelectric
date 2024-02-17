from django.urls import path
from . import views

urlpatterns = [
    path('control_diario/', views.control_diario, name='control_diario'),
    path('control_diario/<int:mes>/<int:año>/', views.control_diario, name='control_diario_fecha'),
    path('menu-control-diario/<int:dia>/<int:mes>/<int:año>/', views.menu_control_diario, name='menu_control_diario'),
    path('obras_por_dia/<int:dia>/<int:mes>/<int:año>/', views.obras_por_dia, name='obras_por_dia'),
    path('emergencias_por_dia/<int:dia>/<int:mes>/<int:año>/', views.emergencias_por_dia, name='emergencias_por_dia'),
    path('reporte_retiro_material/<str:fecha1>/<str:fecha2>/', views.creaAllPdf, name='reporte_retiro_material'),
    path('reporte_devolucion_material/<str:fecha1>/<str:fecha2>/', views.creaBllPdf, name='reporte_devolucion_material'),
    path('creaAllPdf/', views.creaAllPdf, name='creaAllPdf'),
    path('creaBllPdf/', views.creaBllPdf, name='creaBllPdf'),
    path('retiros_pendientes/', views.retiros_pendientes, name='retiros_pendientes'),
    path('devoluciones_pendientes/', views.devoluciones_pendientes, name='devoluciones_pendientes'),
    path('cambiar_etapa_obra/<str:id_obra>/<int:dia>/<int:mes>/<int:año>/', views.cambiar_etapa_obra, name='cambiar_etapa_obra'),
    # Otras rutas...
]