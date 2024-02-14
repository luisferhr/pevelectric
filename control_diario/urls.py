from django.urls import path
from . import views

urlpatterns = [
    path('control_diario/', views.control_diario, name='control_diario'),
    path('control_diario/<int:año>/<int:mes>/', views.control_diario, name='control_diario_fecha'),
    path('obras_por_dia/<int:dia>/<int:mes>/<int:año>/', views.obras_por_dia, name='obras_por_dia'),
]