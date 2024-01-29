from django.shortcuts import render, redirect
from usuario.models import Obra
from .forms import ObraForm

def obras_construccion(request):
    obras = Obra.objects.all()
    return render(request, 'obras.html', {'obras': obras})

def crear_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('obras_construccion')  # Redirige a la página de obras después de crear una nueva obra
    else:
        form = ObraForm()
    return render(request, 'crear_obra.html', {'form': form})