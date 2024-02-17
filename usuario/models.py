from django.db import models
from django.contrib.auth.models import User
from datetime import date
class Obra(models.Model):
    id_obra = models.CharField(max_length=20, primary_key=True)
    descripcion = models.CharField(max_length=45)
    lugar = models.CharField(max_length=45)
    fecha_inicio = models.DateField(default=date.today, blank=True)
    si_finalizo = models.BooleanField(default=False, blank=True)
    etapa= models.IntegerField(default=1, blank=True)
    tipo_obra = models.CharField(max_length=45, blank=True)
class TipoMaterial(models.Model):
    idMaterial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, unique=True)
    descripcion = models.CharField(max_length=45)
    stock = models.IntegerField(default=0)
class RetiroMaterial(models.Model):
    obra = models.ForeignKey(Obra, related_name='retiros_material', on_delete=models.CASCADE)
    tipo_material = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE)
    cantidad_retirada = models.IntegerField(default=0)
    fecha_retiro = models.DateField(default=date.today)
class DevolucionMaterial(models.Model):
    obra = models.ForeignKey(Obra, related_name='devoluciones_material', on_delete=models.CASCADE)
    conductor = models.CharField(max_length=45, blank=True)
    nota_de_pedido = models.CharField(max_length=10, blank=True)
    tipo_material = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE)
    cantidad_devuelta = models.IntegerField(default=0)
    fecha_devolucion = models.DateField(default=date.today)
class Factura(models.Model):
    orden_factura = models.AutoField(primary_key=True)
    obra = models.ForeignKey('Obra', on_delete=models.CASCADE, related_name='facturas')
    num_factura = models.CharField(max_length=100, unique=True, null=False)
    num_nota_credit = models.CharField(max_length=100, unique=True, null=False)
    val_neto_fact = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    val_neto_nc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        indexes = [
            models.Index(fields=['obra'], name='index_obra'),
            models.Index(fields=['num_factura'], name='index_num_factura'),
            models.Index(fields=['num_nota_credit'], name='index_num_nota_credit'),
        ]
    def __str__(self):
        return f"Factura {self.num_factura} para la Obra {self.obra.id_obra}"
class PrimerUsoDia(models.Model):
    fecha = models.DateField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    si_ingresa = models.BooleanField(default=True)
    class Meta:
        indexes = [
            models.Index(fields=['fecha'], name='index_fecha'),
            models.Index(fields=['usuario'], name='index_usuario'),
        ]
    def __str__(self):
        return f"Primer uso de {self.usuario} el {self.fecha}"
class Emergencia(models.Model):
    id_emergencia = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    lugar = models.CharField(max_length=45)
    fecha_inicio = models.DateField(default=date.today)
    
    def __str__(self):
        return f"Emergencia {self.id_emergencia} del dia {self.fecha_inicio}"