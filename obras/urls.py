from django.urls import path
from . import views

urlpatterns = [
    path('obras/', views.obras_construccion, name='obras_construccion'),
    path('crear_obra/', views.crear_obra, name='crear_obra'),
    path('obras/retiro/<str:obra_id>/', views.retiro, name='retiro'),
    path('obras/devolucion/<str:obra_id>/', views.devolucion, name='devolucion'),
    path('modificar_obra/<str:id_obra>/<str:retornar_a>/', views.modificar_obra, name='modificar'),
    path('obras/generar_pdf/<str:obra_id>/', views.generar_pdf, name='generar_pdf'),
    path('obras/borra_retiro/<str:obra_id>/', views.borra_retiro, name='borra_retiro'),
]