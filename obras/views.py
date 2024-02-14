from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usuario.models import Obra, RetiroMaterial, TipoMaterial, DevolucionMaterial
from .forms import ObraSimpleForm, RetiroForm, DevolucionForm, ObraModificaForm
from datetime import date, datetime, timezone
from django.db import transaction
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from django.contrib.staticfiles import finders

@login_required(login_url='/login/')
def obras_construccion(request):
    obras = Obra.objects.all()
    for obra in obras:
        obra.url_retiro = reverse('retiro', args=[obra.id_obra])
        obra.url_devolucion = reverse('devolucion', args=[obra.id_obra])
    return render(request, 'obras.html', {'obras': obras})

@login_required(login_url='/login/')
@transaction.atomic
def crear_obra(request):
    obra_guardada = False
    obra_id = None  
    initial_data = request.session.get('obra_temp', {})
    form = ObraSimpleForm(initial=initial_data)
    if request.method == 'POST':
        form = ObraSimpleForm(request.POST)
        if form.is_valid():
            obra = form.save()
            obra_id = obra.id_obra 
            obra_guardada = True
            request.session['obra_guardada'] = obra_guardada 
            return redirect('obras_construccion')
        else:
            obra_guardada = False
        if obra_guardada:
            if 'retiro' in request.POST:
                return redirect('retiro', obra_id=obra_id)
            elif 'devolucion' in request.POST:
                return redirect('devolucion', obra_id=obra_id)
            request.session.pop('obra_temp', None)
    obra_guardada = request.session.get('obra_guardada', False)
    contexto = {
        'form': form,
        'obra_guardada': obra_guardada,
        'obra_id': obra_id,}
    return render(request, 'crear_obra.html', contexto)
@login_required(login_url='/login/')
def retiro(request, obra_id):
    try:
        obra = Obra.objects.get(id_obra=obra_id)
        print(obra)
    except Obra.DoesNotExist:
        return render(request, 'no_existe.html', {'obra_id': obra_id, 'volver_a': obras_construccion})
    if request.method == 'POST':
        form = RetiroForm(obra=obra, data=request.POST)
        if form.is_valid():
            for name, value in form.cleaned_data.items():
                if value >= 0:
                    id_material = name.split("_")[1]
                    tipo_material = get_object_or_404(TipoMaterial, idMaterial=id_material)
                    RetiroMaterial.objects.update_or_create(
                        obra=obra,
                        tipo_material=tipo_material,
                        defaults={'cantidad_retirada': value}
                    )
            return redirect('obras_construccion')
    else:
        form = RetiroForm(obra=obra)
    return render(request, 'retiro.html', {'form': form, 'obra': obra})

@login_required(login_url='/login/')
def devolucion(request, obra_id):
    try:
        obra = Obra.objects.get(id_obra=obra_id)
        print(obra)
    except Obra.DoesNotExist:
        return render(request, 'no_existe.html', {'obra_id': obra_id, 'volver_a': obras_construccion})
    if request.method == 'POST':
        form = DevolucionForm(obra=obra, data=request.POST)
        if form.is_valid():
            # Procesa cada campo del formulario validado
            for name, value in form.cleaned_data.items():
                if value >= 0:  # Asegura que la cantidad es positiva
                    # El ID del material se extrae del nombre del campo
                    id_material = int(name.split("_")[1])
                    tipo_material = get_object_or_404(TipoMaterial, idMaterial=id_material)
                    # Crea o actualiza el registro de devolución
                    DevolucionMaterial.objects.update_or_create(
                        obra=obra,
                        tipo_material=tipo_material,
                        defaults={'cantidad_devuelta': value}
                    )
            return redirect('obras_construccion')  # Redirecciona tras el éxito
        else:
            # Maneja el caso de un formulario no válido
            return render(request, 'devolucion.html', {'form': form, 'obra': obra, 'error': 'Formulario no válido.'})
    else:
        # Inicializa un formulario en una solicitud GET
        form = DevolucionForm(obra=obra)
    return render(request, 'devolucion.html', {'form': form, 'obra': obra})

@login_required(login_url='/login/')
@transaction.atomic
def modificar_obra(request, id_obra, retornar_a='index'):
    obra = get_object_or_404(Obra, id_obra=id_obra)
    
    if request.method == 'POST':
        form = ObraModificaForm(request.POST, instance=obra)
        if form.is_valid():
            obra_modificada = form.save(commit=False)
            if form.cleaned_data['si_finalizo']:
                obra_modificada.fecha_termino = datetime.date.today()
            obra_modificada.save()
            messages.success(request, 'Obra modificada con éxito.')
            return redirect(retornar_a)
    else:
        form = ObraModificaForm(instance=obra)
    
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
    # Redirige a la vista de retiro para la obra específica
    return redirect('retiro', obra_id=obra_id)

@login_required(login_url='/login/')
def generar_pdf(request, obra_id):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Definir variables para estilo
    estilo_titulo = ("Helvetica-Bold", 20)
    estilo_contenido = ("Helvetica", 12)
    estilo_subtitulo = ("Helvetica-Bold", 12)

    # Dimensiones de la página
    width, height = letter

    # Aplicar estilo de título
    p.setFont(*estilo_titulo)
    p.drawCentredString(width / 2, height - 72, "Empresa Pevelectric")  # Corregido para usar la variable de estilo

    # Incluir imagen
    image_path = finders.find('image.jpg')
    p.drawImage(image_path, 3.5*cm, height - 6*cm, width=2*cm, height=2*cm, mask='auto')  # Corrido 2 cm hacia la izquierda

    # Aplicar estilo de contenido y alineación derecha para fecha y usuario
    p.setFont(*estilo_contenido)
    fecha = f"Fecha de impresión: {datetime.now().strftime('%d/%m/%Y')}"
    usuario = f"Usuario: {request.user.username}"
    p.drawRightString(width - 72, height - 150, fecha)
    p.drawRightString(width - 72, height - 165, usuario)

    p.setFont(*estilo_subtitulo)  # Aplicar estilo de título para "Listado de materiales"
    p.drawCentredString(width / 2, height - 200, "Listado de materiales:")
    p.drawCentredString(width / 2, height - 199, "                  ")
    p.drawCentredString(width / 2, height - 198, "                  ")
    # Espacio después del usuario
    y = height - 250  # Iniciar después de 4 líneas vacías
    obra = Obra.objects.get(id_obra=obra_id)
    for retiro in RetiroMaterial.objects.filter(obra=obra):
        p.setFont(*estilo_contenido)
        material_info = f"{retiro.tipo_material.nombre}"
        p.drawString(100, y, material_info)
        p.setFont(*estilo_subtitulo)
        if retiro.cantidad_retirada == 0:
            material_info = "NO.-"
        else:
            material_info = f"{retiro.cantidad_retirada} unidades"
        p.drawString(300, y, material_info) 
        y -= 30

    # Firmas
    y -= 80  # Dejar espacio antes de las firmas
    p.drawString(100, y, "__________________")
    p.drawString(width - 250, y, "__________________")  # Asegurarse de que no se salga de la página
    p.drawString(110, y-15, "Firma")
    p.drawString(width - 240, y-15, "Firma")

    # Finalizar PDF
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='retiro_material.pdf')