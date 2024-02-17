from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from emergencias.forms import CrearEmergenciaForm, ModificarEmergenciaForm
from usuario.models import Emergencia, Obra

@login_required(login_url='/login/')
def mostrar_emergencias(request):
    emergencias = Emergencia.objects.all()
    return render(request, 'emergencias.html', {'emergencias': emergencias})

@login_required(login_url='/login/')
def crear_emergencia(request):
    if request.method == 'POST':
        form = CrearEmergenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mostrar_emergencias')
    else:
        form = CrearEmergenciaForm()
    return render(request, 'crear_emergencia.html', {'form': form})

@login_required
@transaction.atomic
def modificar_emergencia(request, id_emergencia, retornar_a):
    emergencia = get_object_or_404(Emergencia, pk=id_emergencia)
    if request.method == 'POST':
        form = ModificarEmergenciaForm(request.POST, instance=emergencia)
        if form.is_valid():
            numero_obra = form.cleaned_data.get('numero_obra')
            if numero_obra:
                obra = Obra(
                    id_obra=numero_obra,
                    descripcion=emergencia.descripcion,
                    lugar=emergencia.lugar,
                    fecha_inicio=emergencia.fecha_inicio,
                )
                obra.save()
                emergencia.delete() 
                return redirect(retornar_a)
            form.save()  # Solo actualiza la emergencia si no se proporciona número de obra
            return redirect(retornar_a)
    else:
        form = ModificarEmergenciaForm(instance=emergencia)
    return render(request, 'modificar_emergencia.html', {'form': form, 'retornar_a': retornar_a})