from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usuario.models import Obra, MaterialObra
from .forms import ObraSimpleForm, RetiroForm

@login_required(login_url='/login/')
def obras_construccion(request):
    obras = Obra.objects.all()
    return render(request, 'obras.html', {'obras': obras})

@login_required(login_url='/login/')
def crear_obra(request):
    if request.method == 'POST':
        form = ObraSimpleForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('obras_construccion')
        else:
            print(form.errors)
    else:
        form = ObraSimpleForm()
    return render(request, 'crear_obra.html', {'form': form})

def retiro(request, obra_id):
    obra = Obra.objects.get(id_obra=obra_id)
    if request.method == 'POST':
        form = RetiroForm(request.POST)
        if form.is_valid():
            for name, value in form.cleaned_data.items():
                if value: 
                    tipo_material_id = name.split("_")[1]
                    MaterialObra.objects.create(
                        obra=obra,
                        tipo_material_id=tipo_material_id,
                        retirado=value
                    )
            return redirect('crear_obra')  
    else:
        form = RetiroForm()
    return render(request, 'retiro.html', {'form': form, 'obra_id': obra_id})