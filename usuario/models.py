from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Modelo Obra
class Obra(models.Model):
    id_obra = models.CharField(max_length=45, primary_key=True)
    descripcion = models.CharField(max_length=45)
    lugar = models.CharField(max_length=45)
    si_emergencia = models.BooleanField(default=False)
    si_retira = models.BooleanField(default=False)
    si_devuelve = models.BooleanField(default=False)
    fecha_inicio = models.DateField(default=date.today)  
    fecha_termino = models.DateField(default=date.today)  
    si_finalizo = models.BooleanField(default=False)
    tipo_obra = models.CharField(max_length=45, blank=True)  

    def add_material(self, tipo_material, retirado, devuelto):
        MaterialObra.objects.create(
            obra=self,
            tipo_material=tipo_material,
            retirado=retirado,
            devuelto=devuelto
        )

# Modelo para tipos de materiales
class TipoMaterial(models.Model):
    nombre = models.CharField(max_length=45)
    # Otros campos específicos para cada tipo de material si es necesario

# Modelo que relaciona la obra con los materiales usados/devueltos
class MaterialObra(models.Model):
    obra = models.ForeignKey(Obra, related_name='materiales', on_delete=models.CASCADE)
    tipo_material = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE)
    retirado = models.IntegerField(default=0)
    devuelto = models.IntegerField(default=0)

    class Meta:
        unique_together = ('obra', 'tipo_material')

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