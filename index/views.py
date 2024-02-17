from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuario.models import PrimerUsoDia

@login_required(login_url='/login/')
def index(request):
    hoy = timezone.now().date()
    try:
        primer_uso = PrimerUsoDia.objects.get(fecha=hoy, usuario=request.user)
        primer_uso.si_ingresa = True
        primer_uso.save()
    except PrimerUsoDia.DoesNotExist:
        primer_uso = PrimerUsoDia.objects.create(fecha=hoy, usuario=request.user, si_ingresa=False)
    puede_ingresar = primer_uso.si_ingresa
    return render(request, 'index/index.html', {
        'user': request.user,
        'puede_ingresar': puede_ingresar
    })

def profile(request):
    return render(request, 'index/index.html', {
        'user': request.user
    })