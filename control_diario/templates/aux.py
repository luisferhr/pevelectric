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
    emergencias_del_dia = Emergencia.objects.filter(fecha_inicio=fecha_seleccionada)   
    return render(request, 'obras_por_dia.html', {'obras': obras_del_dia,'emergencias':emergencias_del_dia ,'fecha': fecha_seleccionada})
