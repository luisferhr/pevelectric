# Generated by Django 5.0.1 on 2024-01-28 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('idmaterial', models.AutoField(primary_key=True, serialize=False)),
                ('devolucion', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'material',
            },
        ),
        migrations.CreateModel(
            name='TipoMaterial',
            fields=[
                ('idtipo_material', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'tipo_material',
            },
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('numero_obra', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=45)),
                ('lugar', models.CharField(max_length=45)),
                ('apoyo_data', models.CharField(blank=True, max_length=45, null=True)),
                ('material', models.ForeignKey(db_column='material_idmaterial', on_delete=django.db.models.deletion.CASCADE, to='usuario.material')),
                ('usuario', models.ForeignKey(db_column='Usuario_idUsuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Obra',
            },
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('idcontrarto', models.AutoField(primary_key=True, serialize=False)),
                ('oficina', models.CharField(blank=True, max_length=45, null=True)),
                ('carta_de_termino', models.CharField(blank=True, max_length=45, null=True)),
                ('obra', models.ForeignKey(db_column='Obra_numero_obra', on_delete=django.db.models.deletion.CASCADE, to='usuario.obra')),
            ],
            options={
                'db_table': 'contrato',
            },
        ),
        migrations.CreateModel(
            name='Apoyo',
            fields=[
                ('idapoyo', models.AutoField(primary_key=True, serialize=False)),
                ('ot_o_pm', models.CharField(blank=True, db_column='OT_o_PM', max_length=45, null=True)),
                ('obra', models.ForeignKey(db_column='Obra_numero_obra', on_delete=django.db.models.deletion.CASCADE, to='usuario.obra')),
            ],
            options={
                'db_table': 'apoyo',
            },
        ),
        migrations.AddField(
            model_name='material',
            name='tipo_material',
            field=models.ForeignKey(db_column='tipo_material_idtipo_material', on_delete=django.db.models.deletion.CASCADE, to='usuario.tipomaterial'),
        ),
    ]
