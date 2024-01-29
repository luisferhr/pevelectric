from django.urls import path
from . import views

urlpatterns = [
    path('prevencion_riesgos/', views.prevencion_riesgos, name='prevencion_riesgos'),
]