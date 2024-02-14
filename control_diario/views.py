#views.py
from datetime import date, datetime, timedelta
import locale, calendar, json
from django.shortcuts import render
from django.urls import reverse
from usuario.models import Obra

def control_diario(request, año=None, mes=None):
    try:
       locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Ajusta según tu sistema/ubicación
    except locale.Error:
       locale.setlocale(locale.LC_TIME, 'es')  # Intenta un código más genérico si el específico falla

    hoy = datetime.today()
    if año is None and mes is None:
        año = hoy.year
        mes = hoy.month
    else:
        año = int(año) if año is not None else hoy.year
        mes = int(mes) if mes is not None else hoy.month
    año = int(año)
    mes = int(mes)
    # Determina el mes y año siguiente
    if mes == 12:
        mes_siguiente = 1
        año_siguiente = año + 1
    else:
        mes_siguiente = mes + 1
        año_siguiente = año
    # Determina el mes y año anterior
    if mes == 1:
        mes_anterior = 12
        año_anterior = año - 1
    else:
        mes_anterior = mes - 1
        año_anterior = año
    año_antes = año - 1
    año_despues = año + 1   
    #Limpiamos semana
    semana = [[0 for _ in range(7)] for _ in range(6)]
    semana = fill_calendar_matrix(mes, año)
    #semana ya tiene los dias de la semana
    semana = [semana for semana in semana if any(dia != 0 for dia in semana)]
    hay_obras = fill_calendar_matrix_trabajos(mes, año, semana)
    inicio_obra = crearJsonInicioObra(mes, año, semana)
    print(inicio_obra)
    print("_____________________________")
    print("                             ")
    dias_con_obras = []
    for semana_dias, semana_obras in zip(semana, hay_obras):
        semana_combinada = []
        for dia, tiene_obra in zip(semana_dias, semana_obras):
            semana_combinada.append({'dia': dia, 'tiene_obra': tiene_obra})
        dias_con_obras.append(semana_combinada)
    context = {
        'año': año,
        'mes': mes,
        'nombre_mes': calendar.month_name[mes],
        'semanas': dias_con_obras,
        'hay_obras': hay_obras,
        'mes_siguiente': mes_siguiente,
        'año_siguiente': año_siguiente,
        'mes_anterior': mes_anterior,
        'año_anterior': año_anterior,
        'año_antes': año_antes,
        'año_despues': año_despues,
        'inicio_obra': inicio_obra,  
    }
    return render(request, 'calendario.html', context)

def obras_por_dia(request, dia=1, mes=1, año=2021):
    return render(request, 'obras_por_dia.html')

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