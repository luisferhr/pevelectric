from django.urls import path
from . import views

urlpatterns = [
    path('control_diario/', views.control_diario, name='control_diario'),
]