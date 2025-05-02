import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Min, Max
from .models import Producto, ColorProducto, TallaVariante

def index(request):
    return render(request, 'index.html')

def catalogo(request):
    productos = Producto.objects.all()
    productos_con_datos = []

    for producto in productos:
        variantes = TallaVariante.objects.filter(color_producto__producto=producto)
        agregados = variantes.aggregate(
            total_stock=Sum('stock'),
            precio_min=Min('precio'),
            precio_max=Max('precio')
        )
        productos_con_datos.append({
            'producto': producto,
            'total_stock': agregados['total_stock'] or 0,
            'precio_min': agregados['precio_min'] or 0,
            'precio_max': agregados['precio_max'] or 0,
        })

        print(agregados)

    return render(request, 'catalogo.html', {
        'productos_con_datos': productos_con_datos,
    })


def producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    colores = ColorProducto.objects.filter(producto=producto).select_related('color')

    # Crear un diccionario para pasar colores y tallas de manera ordenada
    color_tallas = {}
    variantes_data = []

    for color_producto in colores:
        tallas = TallaVariante.objects.filter(color_producto=color_producto).select_related('talla')
        color_tallas[color_producto] = tallas

        # Construir lista de variantes
        for talla_variante in tallas:
            variantes_data.append({
                'color_id': color_producto.id,
                'color_nombre': color_producto.color.nombre,
                'talla_id': talla_variante.talla.id,
                'talla_nombre': talla_variante.talla.nombre,
                'sku': talla_variante.sku,
                'precio': float(talla_variante.precio),
                'stock': talla_variante.stock,
                'imagen': color_producto.imagen_color.url if color_producto.imagen_color else '',
            })

    contexto = {
        'producto': producto,
        'colores': colores,
        'color_tallas': color_tallas,
        'variantes_json': json.dumps(variantes_data, cls=DjangoJSONEncoder),
    }

    return render(request, 'producto.html', contexto)

def favoritos(request):
    return render(request, 'favoritos.html')

def contacto(request):
    return render(request, 'contacto.html')