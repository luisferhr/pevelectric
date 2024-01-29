from django.db import models

from django.db import models
from django.contrib.auth.models import User

class TipoMaterial(models.Model):
    idtipo_material = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'tipo_material'

class Material(models.Model):
    idmaterial = models.AutoField(primary_key=True)
    tipo_material = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE, db_column='tipo_material_idtipo_material')
    devolucion = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)

    class Meta:
        db_table = 'material'

class Obra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='Usuario_idUsuario')
    numero_obra = models.CharField(primary_key=True, max_length=45)
    descripcion = models.CharField(max_length=45)
    lugar = models.CharField(max_length=45)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, db_column='material_idmaterial')
    apoyo_data = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'Obra'

class Apoyo(models.Model):
    idapoyo = models.AutoField(primary_key=True)
    ot_o_pm = models.CharField(db_column='OT_o_PM', max_length=45, blank=True, null=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, db_column='Obra_numero_obra')

    class Meta:
        db_table = 'apoyo'

class Contrato(models.Model):
    idcontrarto = models.AutoField(primary_key=True)
    oficina = models.CharField(max_length=45, blank=True, null=True)
    carta_de_termino = models.CharField(max_length=45, blank=True, null=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, db_column='Obra_numero_obra')

    class Meta:
        db_table = 'contrato'