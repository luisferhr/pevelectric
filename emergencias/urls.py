from django.urls import path
from . import views

urlpatterns = [
    path('mostrar_emergencias/', views.mostrar_emergencias, name='mostrar_emergencias'),
    path('crear_emergencia/', views.crear_emergencia, name='crear_emergencia'),
    path('modificar_emergencia/<int:id_emergencia>/<str:retornar_a>/', views.modificar_emergencia, name='modificar_emergencia'),
]