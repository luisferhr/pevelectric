from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('obras/', include('obras.urls')), 
    path('emergencias/', include('emergencias.urls')),
    path('control_diario/', include('control_diario.urls')),
    path('facturacion/', include('facturacion.urls')),
    path('remuneracion/', include('remuneracion.urls')),
    path('prevencion_riesgos/', include('prevencion_riesgos.urls')),
]