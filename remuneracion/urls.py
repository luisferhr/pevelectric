
from django.urls import path
from . import views

urlpatterns = [
    path('remuneracion/', views.remuneracion, name='remuneracion'),
]