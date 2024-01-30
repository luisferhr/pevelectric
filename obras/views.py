from django.shortcuts import render, redirect
from usuario.models import Obra, Material
from .forms import ObraSimpleForm

def obras_construccion(request):
    obras = Obra.objects.all()
    return render(request, 'obras.html', {'obras': obras})

def crear_obra(request):
    if request.method == 'POST':
        form = ObraSimpleForm(request.POST)
        if form.is_valid():
            id_material = form.cleaned_data.get('fk_material')
            material, created = Material.objects.get_or_create(id_material=id_material)
            if created:
                material.save()
            obra = Obra(
                id_obra=form.cleaned_data.get('id_obra'),
                descripcion=form.cleaned_data.get('descripcion'),
                lugar=form.cleaned_data.get('lugar'),
                fk_material=material,
                emergencia=form.cleaned_data.get('emergencia')
            )
            obra.save()
            return redirect('obras_construccion')
        else:
            print(form.errors)
    else:
        form = ObraSimpleForm()
    return render(request, 'crear_obra.html', {'form': form})
                
            