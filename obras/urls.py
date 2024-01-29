from django.urls import path
from . import views

urlpatterns = [
    path('obras/', views.obras_construccion, name='obras_construccion'),
    path('crear_obra/', views.crear_obra, name='crear_obra'),
]