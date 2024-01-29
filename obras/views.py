from django.shortcuts import render

def obras_construccion(request):
    return render(request, 'obras.html')