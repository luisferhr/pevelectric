from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
    id_material = models.CharField(max_length=45,primary_key=True)
    tipo_material = models.CharField(max_length=45)
    devolucion = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)
    class Meta:
        db_table = 'material'

class Obra(models.Model):
    id_obra = models.CharField(max_length=45,primary_key=True)
    descripcion = models.CharField(max_length=45)
    lugar = models.CharField(max_length=45)
    fk_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    emergencia = models.BooleanField(default=False)
    class Meta:
        db_table = 'Obra'

class Contrato(models.Model):
    id_contrato = models.CharField(max_length=45,primary_key=True)
    oficina = models.CharField(max_length=45, blank=True, null=True)
    carta_de_termino = models.CharField(max_length=45, blank=True, null=True)
    fk_obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    class Meta:
        db_table = 'contrato'