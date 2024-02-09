from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')  # Redirige a login si no está autenticado
def index(request):
    return render(request, 'index/index.html', {
        'user': request.user
    })

def profile(request):
    return render(request, 'index/index.html', {
        'user': request.user
    })