#views.py
from reportlab.lib.units import cm
from datetime import date, datetime, timedelta
import locale, calendar, json, io
from tkinter import Canvas
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from usuario.models import Obra, RetiroMaterial, TipoMaterial, PrimerUsoDia, DevolucionMaterial, Emergencia
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from django.contrib.staticfiles import finders
from django.utils import timezone

@login_required(login_url='/login/')
def menu_control_diario(request, dia=None, mes=None, año=None):
    contexto = {
        'dia': dia,
        'mes': mes,
        'año': año,
    }
    return render(request, 'menu_control_diario_OE.html', contexto)

@login_required(login_url='/login/')
def control_diario(request, año=None, mes=None):
    puede_ingresar = True
    try:
       locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Ajusta según tu sistema/ubicación
    except locale.Error:
       locale.setlocale(locale.LC_TIME, 'es')  # Intenta un código más genérico si el específico falla
    hoy = timezone.now().date()
    if año is None and mes is None:
        año = hoy.year
        mes = hoy.month
    else:
        año = int(año) if año is not None else hoy.year
        mes = int(mes) if mes is not None else hoy.month
    año = int(año)
    mes = int(mes)
    if mes == 12:
        mes_siguiente = 1
        año_siguiente = año + 1
    else:
        mes_siguiente = mes + 1
        año_siguiente = año
    if mes == 1:
        mes_anterior = 12
        año_anterior = año - 1
    else:
        mes_anterior = mes - 1
        año_anterior = año
    año_antes = año - 1
    año_despues = año + 1
    fecha1 = f"{año}-{mes:02d}-01"
    fecha2 = f"{año}-{mes:02d}-{calendar.monthrange(año, mes)[1]}"
    mes_mostrar = [[0 for _ in range(7)] for _ in range(6)]
    mes_mostrar = fill_calendar_matrix(mes, año)
    mes_mostrar = [mes_mostrar for mes_mostrar in mes_mostrar if any(dia != 0 for dia in mes_mostrar)]
    hay_obras = fill_calendar_matrix_trabajos(mes, año, mes_mostrar)
    inicio_obra = crearJsonInicioObra(mes, año, mes_mostrar)
    dias_con_obras = []
    for semana_dias, semana_obras in zip(mes_mostrar, hay_obras):
        semana_combinada = []
        for dia, tiene_obra in zip(semana_dias, semana_obras):
            semana_combinada.append({'dia': dia, 'tiene_obra': tiene_obra})
        dias_con_obras.append(semana_combinada)
    context = {
        'año': año,
        'mes': mes,
        'nombre_mes': calendar.month_name[mes],
        'mes_mostrar': dias_con_obras,
        'hay_obras': hay_obras,
        'mes_siguiente': mes_siguiente,
        'año_siguiente': año_siguiente,
        'mes_anterior': mes_anterior,
        'año_anterior': año_anterior,
        'año_antes': año_antes,
        'año_despues': año_despues,
        'inicio_obra': inicio_obra, 
        'fecha1': fecha1,
        'fecha2': fecha2,
        'puede_ingresar': puede_ingresar,
    }
    return render(request, 'calendario.html', context)

@login_required(login_url='/login/')
def obras_por_dia(request, dia=1, mes=1, año=2021):
    hoy = timezone.now().date()
    primer_uso, created = PrimerUsoDia.objects.get_or_create(
        fecha=hoy, 
        usuario=request.user, 
        defaults={'si_ingresa': False}
    )
    puede_ingresar = primer_uso.si_ingresa
    fecha_seleccionada = date(year=año, month=mes, day=dia)
    obras_del_dia = Obra.objects.filter(fecha_inicio=fecha_seleccionada)
    context = {
        'obras': obras_del_dia,
        'fecha': fecha_seleccionada,
        'dia': dia,
        'mes': mes,
        'año': año,
        'puede_ingresar': puede_ingresar 
    }
    return render(request, 'obras_por_dia.html', context)

@login_required(login_url='/login/')
def emergencias_por_dia(request, dia=1, mes=1, año=2021):
    hoy = timezone.now().date()
    primer_uso, created = PrimerUsoDia.objects.get_or_create(
        fecha=hoy, 
        usuario=request.user, 
        defaults={'si_ingresa': False}
    )
    puede_ingresar = primer_uso.si_ingresa
    fecha_seleccionada = date(year=año, month=mes, day=dia)
    emergencias_del_dia = Emergencia.objects.filter(fecha_inicio=fecha_seleccionada)
    return render(request, 'emergencias_por_dia.html', {'emergencias': emergencias_del_dia, 'fecha': fecha_seleccionada})

def num_fecha(dia, mes, año):
    try:
        date = datetime(año, mes, dia)
        return date.weekday()
    except ValueError as e:
        return f"Error: {str(e)}"
 
def fill_calendar_matrix(mes, año):
    num_dias_mes = calendar.monthrange(año, mes)[1]
    semana = [[0 for _ in range(7)] for _ in range(6)]
    inicio = num_fecha(1, mes, año)
    dia_actual = 1
    semana_actual = 0
    while dia_actual <= num_dias_mes:
        if inicio > 6:
            semana_actual += 1
            inicio = 0
        semana[semana_actual][inicio] = dia_actual
        dia_actual += 1
        inicio += 1
    return semana

def fill_calendar_matrix_trabajos(mes, año, semana):
    fecha_inicio_mes = datetime(año, mes, 1).date()
    ultimo_dia_mes = calendar.monthrange(año, mes)[1]
    fecha_fin_mes = datetime(año, mes, ultimo_dia_mes).date()
    trabajos_activos_del_mes = Obra.objects.filter(
        fecha_inicio__lte=fecha_fin_mes, 
        si_finalizo=False
    )
    s = len(semana) 
    d = len(semana[0]) 
    hay_obras = [[False for _ in range(d)] for _ in range(s)]
    for obra in trabajos_activos_del_mes:
        dia_inicio = obra.fecha_inicio.day
        mes_inicio = obra.fecha_inicio.month
        año_inicio = obra.fecha_inicio.year
        if mes_inicio == mes and año_inicio == año:
            for i in range(s):
                for j in range(d):
                    if semana[i][j] >= dia_inicio:
                        hay_obras[i][j] = True
    return hay_obras

def crearJsonInicioObra(mes, año, semana):
    inicio_mes = date(año, mes, 1)
    fin_mes = date(año, mes, calendar.monthrange(año, mes)[1])
    obras = Obra.objects.filter(fecha_inicio__gte=inicio_mes, fecha_inicio__lte=fin_mes)
    inicio_obra = {}
    for obra in obras:
        dia = obra.fecha_inicio.day
        if dia not in inicio_obra:
            inicio_obra[dia] = []
        inicio_obra[dia].append(obra.id_obra)
    return json.dumps(inicio_obra)

@login_required(login_url='/login/')
def creaAllPdf(request, fecha1=None, fecha2=None):
    if fecha1 and fecha2:
        fecha_inicio = datetime.strptime(fecha1, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha2, "%Y-%m-%d")
    else:
        fecha_inicio=None
        fecha_fin=None
    try:
       locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Ajusta según tu sistema/ubicación
    except locale.Error:
       locale.setlocale(locale.LC_TIME, 'es')  # Intenta un código más genérico si el específico falla
    estilo_titulo = ('Helvetica-Bold', 16)
    estilo_subtitulo = ('Helvetica-Bold', 12)
    estilo_contenido = ('Helvetica', 10)
    nombres_materiales = TipoMaterial.objects.order_by('nombre').values_list('nombre', flat=True)
    cabecera = ['Obra'] + list(nombres_materiales)
    datos_obras = []
    if fecha_inicio and fecha_fin:
        obras = Obra.objects.filter(fecha_inicio__gte=fecha_inicio, fecha_inicio__lte=fecha_fin).distinct()
    else:
        obras = Obra.objects.all().distinct()
    for obra in obras:
        datos_obra = {'Obra': obra.id_obra}
        if fecha_inicio and fecha_fin:
            retiros = RetiroMaterial.objects.filter(obra=obra, fecha_retiro__range=(fecha_inicio, fecha_fin))
        else:
            retiros = RetiroMaterial.objects.filter(obra=obra)
        suma_cantidades = 0
        for retiro in retiros:
            cantidad_retirada = retiro.cantidad_retirada
            datos_obra[retiro.tipo_material.nombre] = retiro.cantidad_retirada
            suma_cantidades += cantidad_retirada
        if suma_cantidades > 0:
            datos_obras.append(datos_obra)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    y = height - 3*cm
    p.setFont(*estilo_titulo)
    p.drawCentredString(width / 2, y+10, "Empresa Pevelectric")
    y -= 1*cm
    p.setFont(*estilo_subtitulo)
    fecha = f"Fecha de impresión: {datetime.now().strftime('%d/%m/%Y')}"
    usuario = f"Usuario: {request.user.username}"
    p.drawString(width - 10*cm, y, fecha)
    y -= 15
    p.drawString(width - 10*cm, y, usuario)
    image_path = finders.find('image.jpg')
    if image_path:
        p.drawImage(image_path, 3.5*cm, y - 0.5*cm, width=2*cm, height=2*cm, mask='auto') 
    y = y-50
    if fecha_inicio and fecha_fin:
        p.drawString(width - 20*cm, y, f"Resumen de los retiros del mes {fecha_inicio.strftime('%B')} de {fecha_inicio.year}")
    else:
        p.drawString(width - 20*cm, y, f"Resumen de los retiros pendientes de materiales")
    y = y-50
    p.setFont(*estilo_subtitulo)
    for i, nombre in enumerate(cabecera):
        p.drawString(30 + i*100, y, nombre)
    y = y -30
    p.setFont(*estilo_contenido)
    for obra in datos_obras:
        for i, nombre in enumerate(cabecera):
            valor = obra.get(nombre, 0)
            if valor == 0:
               material_info = "NO"
            elif nombre.lower() in ['ferreteria', 'ferretería']:
               material_info = "SI" if valor > 0 else "NO"
            else:
               material_info = f"{valor}"
            p.drawString(30 + i*100, y, str(material_info))
        y -= 20
        # Control de salto de página
        if y < 50:
            p.showPage()
            y = height - 50  # Reiniciar `y` para la nueva página
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_retiro_material.pdf')

@login_required(login_url='/login/')
def creaBllPdf(request, fecha1=None, fecha2=None):
    if fecha1 and fecha2:
        fecha_inicio = datetime.strptime(fecha1, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha2, "%Y-%m-%d")
    else:
        fecha_inicio = None
        fecha_fin = None
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'es')
    estilo_titulo = ('Helvetica-Bold', 16)
    estilo_subtitulo = ('Helvetica-Bold', 12)
    estilo_contenido = ('Helvetica', 10)
    nombres_materiales = TipoMaterial.objects.order_by('nombre').values_list('nombre', flat=True)
    cabecera = ['Obra'] + list(nombres_materiales)
    datos_obras = []
    if fecha_inicio and fecha_fin:
        obras = Obra.objects.filter(fecha_inicio__gte=fecha_inicio, fecha_inicio__lte=fecha_fin).distinct()
    else:
        obras = Obra.objects.all().distinct()
    for obra in obras:
        datos_obra = {'Obra': obra.id_obra}
        devoluciones = DevolucionMaterial.objects.filter(obra=obra, fecha_devolucion__range=(fecha_inicio, fecha_fin)) if fecha_inicio and fecha_fin else DevolucionMaterial.objects.filter(obra=obra)
        suma_cantidades = 0
        for devolucion in devoluciones:
            cantidad_devuelta = devolucion.cantidad_devuelta
            datos_obra[devolucion.tipo_material.nombre] = cantidad_devuelta
            suma_cantidades += cantidad_devuelta
        if suma_cantidades > 0:
            datos_obras.append(datos_obra)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    y = height - 3*cm
    p.setFont(*estilo_titulo)
    p.drawCentredString(width / 2, y+10, "Empresa Pevelectric - Reporte de Devoluciones")
    y -= 1*cm
    p.setFont(*estilo_subtitulo)
    fecha = f"Fecha de impresión: {datetime.now().strftime('%d/%m/%Y')}"
    usuario = f"Usuario: {request.user.username}"
    p.drawString(width - 10*cm, y, fecha)
    y -= 15
    p.drawString(width - 10*cm, y, usuario)
    image_path = finders.find('image.jpg')
    if image_path:
        p.drawImage(image_path, 3.5*cm, y - 0.5*cm, width=2*cm, height=2*cm, mask='auto')
    y = y-50
    titulo_reporte = "Resumen de Devoluciones" if fecha_inicio and fecha_fin else "Resumen de Devoluciones Pendientes"
    p.drawString(width - 20*cm, y, titulo_reporte)
    y = y-50
    p.setFont(*estilo_subtitulo)
    for i, nombre in enumerate(cabecera):
        p.drawString(30 + i*100, y, nombre)
    y = y -30
    p.setFont(*estilo_contenido)
    for obra in datos_obras:
        for i, nombre in enumerate(cabecera):
            valor = obra.get(nombre, 0)
            if valor == 0:
               material_info = "NO"
            elif nombre.lower() in ['ferreteria', 'ferretería']:
               material_info = "SI" if valor > 0 else "NO"
            else:
               material_info = f"{valor}"
            p.drawString(30 + i*100, y, str(material_info))
        y -= 20
        # Control de salto de página
        if y < 50:
            p.showPage()
            y = height - 50  # Reiniciar `y` para la nueva página
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_devolucion_material.pdf')

@login_required(login_url='/login/')
def retiros_pendientes(request):
    nombres_materiales = list(TipoMaterial.objects.order_by('nombre').values_list('nombre', flat=True))
    cabecera = ['Obra'] + nombres_materiales
    datos_obras = []
    obras = Obra.objects.all().distinct()
    for obra in obras:
        valores = [0] * len(nombres_materiales)
        datos_obra = {'Obra': obra.id_obra}
        retiros = RetiroMaterial.objects.filter(obra=obra)
        for retiro in retiros:
            indice = nombres_materiales.index(retiro.tipo_material.nombre)
            valores[indice] += retiro.cantidad_retirada
        # Reemplaza los valores de 0 con "NO" y maneja el caso especial de "ferretería"
        for i, cantidad in enumerate(valores):
            if nombres_materiales[i].lower() == "ferretería":
                valores[i] = "SI" if cantidad > 0 else "NO"
            else:
                valores[i] = cantidad if cantidad > 0 else "NO"
        # Añade los valores a datos_obra si hay al menos un retiro no cero o "SI" para ferretería
        if any(cantidad != "NO" for cantidad in valores):
            datos_obra.update(dict(zip(nombres_materiales, valores)))
            datos_obras.append(datos_obra)
    return render(request, 'mostrar_retiros_pendientes.html', {
        'cabecera': cabecera,
        'datos_obras': datos_obras,
    })

@login_required
def cambiar_etapa_obra(request, id_obra, dia, mes, año):
    obra = get_object_or_404(Obra, id_obra=id_obra)
    if obra.etapa < 3:
        obra.etapa += 1
        obra.save()
    url = reverse('obras_por_dia', args=[dia, mes, año])
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def devoluciones_pendientes(request):
    nombres_materiales = list(TipoMaterial.objects.order_by('nombre').values_list('nombre', flat=True))
    cabecera = ['Obra'] + nombres_materiales
    datos_obras = []
    obras = Obra.objects.all().distinct()
    for obra in obras:
        valores = [0] * len(nombres_materiales)
        datos_obra = {'Obra': obra.id_obra}
        devoluciones = DevolucionMaterial.objects.filter(obra=obra)
        for devolucion in devoluciones:
            indice = nombres_materiales.index(devolucion.tipo_material.nombre)
            valores[indice] += devolucion.cantidad_devuelta
        # Reemplaza los valores de 0 con "NO" y maneja el caso especial de "ferretería"
        for i, cantidad in enumerate(valores):
            if nombres_materiales[i].lower() == "ferretería":
                valores[i] = "SI" if cantidad > 0 else "NO"
            else:
                valores[i] = cantidad if cantidad > 0 else "NO"
        # Añade los valores a datos_obra si hay al menos una devolución no cero o "SI" para ferretería
        if any(cantidad != "NO" for cantidad in valores):
            datos_obra.update(dict(zip(nombres_materiales, valores)))
            datos_obras.append(datos_obra)
    return render(request, 'mostrar_devoluciones_pendientes.html', {
        'cabecera': cabecera,
        'datos_obras': datos_obras,
    })