from django.http import HttpResponse
from django.shortcuts import render 
from .models import Producto

def index(request):
    return render(request, 'index.html')

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

def contacto(request):
    return render(request, 'contacto.html')