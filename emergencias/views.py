from django.shortcuts import render

def emergencias(request):
    return render(request, 'emergencias.html')