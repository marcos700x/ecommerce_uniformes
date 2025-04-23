from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Producto

def index(request):
    return render(request, 'index.html')

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})

def producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'producto.html', {'producto': producto})

def contacto(request):
    return render(request, 'contacto.html')