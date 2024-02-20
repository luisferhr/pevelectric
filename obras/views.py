from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuario.models import Obra, RetiroMaterial, TipoMaterial, DevolucionMaterial
from .forms import CrearObraForm, RetiroForm, DevolucionForm, ModificarObraForm
from datetime import date, datetime
from django.utils import timezone
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from django.contrib.staticfiles import finders
from django.db import transaction

@login_required(login_url='/login/')
def mostrar_obras(request):
    obras = Obra.objects.all()
    for obra in obras:
        obra.url_retiro = reverse('retiro', args=[obra.id_obra])
        obra.url_devolucion = reverse('devolucion', args=[obra.id_obra])
    return render(request, 'obras.html', {'obras': obras})

@login_required(login_url='/login/')
@transaction.atomic
def crear_obra(request):
    if request.method == 'POST':
        form = CrearObraForm(request.POST)
        if form.is_valid():
            obra = form.save(commit=False) 
            obra.fecha_inicio = timezone.now().date()
            obra.save() 
            request.session['obra_guardada'] = True
            return redirect('mostrar_obras')  
    else:
        form = CrearObraForm()  
    contexto = {
        'form': form,
        'obra_guardada': request.session.get('obra_guardada', False),
    }
    return render(request, 'crear_obra.html', contexto)

@login_required(login_url='/login/')
def retiro(request, obra_id):
    try:
        obra = Obra.objects.get(id_obra=obra_id)
        print(obra)
    except Obra.DoesNotExist:
        return render(request, 'no_existe.html', {'obra_id': obra_id, 'volver_a': mostrar_obras})
    if request.method == 'POST':
        form = RetiroForm(obra=obra, data=request.POST)
        if form.is_valid():
            for name, value in form.cleaned_data.items():
                if name == 'si_ferreteria':
                    tipo_material = get_object_or_404(TipoMaterial, nombre__iexact='ferreteria')
                    cantidad_retirada = 10 if value else 0
                    RetiroMaterial.objects.update_or_create(
                        obra=obra,
                        tipo_material=tipo_material,
                        defaults={'cantidad_retirada': cantidad_retirada}
                    )
                elif value >= 0:
                    id_material = name.split("_")[1]
                    tipo_material = get_object_or_404(TipoMaterial, idMaterial=id_material)
                    RetiroMaterial.objects.update_or_create(
                        obra=obra,
                        tipo_material=tipo_material,
                        defaults={'cantidad_retirada': value}
                    )
            return redirect('mostrar_obras')  # Redirecciona tras el éxito
    else:
        form = RetiroForm(obra=obra)
    return render(request, 'retiro.html', {'form': form, 'obra': obra})

@login_required(login_url='/login/')
def devolucion(request, obra_id):
    try:
        obra = Obra.objects.get(id_obra=obra_id)
        print(obra)
    except Obra.DoesNotExist:
        return render(request, 'no_existe.html', {'obra_id': obra_id, 'volver_a': mostrar_obras})
    if request.method == 'POST':
        form = DevolucionForm(obra=obra, data=request.POST)
        if form.is_valid():
            for name, value in form.cleaned_data.items():
                if name == 'si_ferreteria':
                    tipo_material = get_object_or_404(TipoMaterial, nombre__iexact='ferreteria')
                    cantidad_devuelta = 10 if value else 0
                    DevolucionMaterial.objects.update_or_create(
                        obra=obra,
                        tipo_material=tipo_material,
                        defaults={'cantidad_devuelta': cantidad_devuelta}
                    )
                elif value >= 0:
                    id_material = name.split("_")[1]
                    tipo_material = get_object_or_404(TipoMaterial, idMaterial=id_material)
                    DevolucionMaterial.objects.update_or_create(
                        obra=obra,
                        tipo_material=tipo_material,
                        defaults={'cantidad_devuelta': value}
                    )
            return redirect('mostrar_obras')  # Redirecciona tras el éxito
        else:
            return render(request, 'devolucion.html', {'form': form, 'obra': obra, 'error': 'Formulario no válido.'})
    else:
        form = DevolucionForm(obra=obra)
    return render(request, 'devolucion.html', {'form': form, 'obra': obra})

@login_required(login_url='/login/')
@transaction.atomic
def modificar_obra(request, id_obra, retornar_a='mostrar_obras'):
    obra = get_object_or_404(Obra, id_obra=id_obra)
    if request.method == 'POST':
        form = ModificarObraForm(request.POST, instance=obra)
        if form.is_valid():
            obra_modificada = form.save(commit=False)
            if form.cleaned_data['si_finalizo']:
                obra_modificada.fecha_termino = datetime.today().date()
            obra_modificada.save()
            messages.success(request, 'Obra modificada con éxito.')
            return redirect(retornar_a)
    else:
        form = ModificarObraForm(instance=obra)
    
    contexto = {
        'form': form,
        'id_obra': id_obra,
    }
    return render(request, 'modificar_obra.html', contexto)

@login_required(login_url='/login/')
def borra_retiro(request, obra_id):
    obra = get_object_or_404(Obra, id_obra=obra_id)
    retiros = RetiroMaterial.objects.filter(obra=obra)
    for retiro in retiros:
        retiro.cantidad_retirada = 0
        retiro.save()
    messages.success(request, 'Todos los retiros han sido reseteados a cero.')
    return redirect('retiro', obra_id=obra_id)

@login_required(login_url='/login/')
def generar_pdf(request, obra_id):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    estilo_titulo = ("Helvetica-Bold", 20)
    estilo_contenido = ("Helvetica", 12)
    estilo_subtitulo = ("Helvetica-Bold", 12)
    width, height = letter
    p.setFont(*estilo_titulo)
    p.drawCentredString(width / 2, height - 72, "Empresa Pevelectric") 
    image_path = finders.find('image.jpg')
    if image_path:
        p.drawImage(image_path, 3.5*cm, height - 3.5*cm, width=2*cm, height=2*cm, mask='auto') 
    p.setFont(*estilo_contenido)
    fecha = f"Fecha de impresión: {datetime.now().strftime('%d/%m/%Y')}"
    usuario = f"Usuario: {request.user.username}"
    p.drawRightString(width - 72, height - 110, fecha)
    p.drawRightString(width - 72, height - 135, usuario)
    p.setFont(*estilo_subtitulo)  # Aplicar estilo de título para "Listado de materiales"
    p.drawCentredString((width / 2)-30, height - 200, "Listado de retiro de materiales:")
    p.drawCentredString((width / 2)-25, height - 220, f"Obra >>> {obra_id}                  ")
    y = height - 300  # Iniciar después de 4 líneas vacías
    obra = Obra.objects.get(id_obra=obra_id)
    for retiro in RetiroMaterial.objects.filter(obra=obra):
        p.setFont(*estilo_contenido)
        material_info = f"{retiro.tipo_material.nombre}"
        p.drawString(180, y, material_info)
        p.setFont(*estilo_subtitulo)
        if retiro.cantidad_retirada == 0:
            material_info = "NO"
        elif retiro.tipo_material.nombre.lower() in ['ferreteria', 'ferretería']:
            material_info = "SI" if retiro.cantidad_retirada > 0 else "NO"
        else:
            material_info = f"{retiro.cantidad_retirada} unidades"
        p.drawString(330, y, material_info) 
        y -= 30
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='retiro_material.pdf')