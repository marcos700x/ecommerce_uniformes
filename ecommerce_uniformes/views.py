import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Min, Max
from .models import Producto, ColorProducto, TallaVariante, Favoritos, Categoria, Talla, Escuela
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from functools import wraps

def index(request):
    return render(request, 'index.html')

def catalogo(request):
    # 1. Leer filtros desde GET
    escuela_ids = request.GET.getlist('escuelas')
    categoria_ids = request.GET.getlist('categorias')
    talla_ids = request.GET.getlist('tallas')
    disponibilidad = request.GET.getlist('disponibilidad')

    # 2. Queryset base de productos
    productos = Producto.objects.all()

    # 3. Filtrar por escuela y categoría
    if escuela_ids:
        productos = productos.filter(escuela__id__in=escuela_ids)
    if categoria_ids:
        productos = productos.filter(categoria__id__in=categoria_ids)

    # 4. Filtrar por tallas
    if talla_ids:
        productos = productos.filter(
            colores__tallas__talla__id__in=talla_ids
        ).distinct()

    # 5. Filtrar por disponibilidad (revertimos al método por suma de stocks)
    if disponibilidad:
        # obtenemos para cada producto la suma de stock de todas sus variantes
        agg_by_prod = (
            TallaVariante.objects
            .values('color_producto__producto_id')
            .annotate(total=Sum('stock'))
        )
        disponibles_ids = []
        for entry in agg_by_prod:
            pid = entry['color_producto__producto_id']
            total = entry['total'] or 0
            if 'disponible' in disponibilidad and total > 0:
                disponibles_ids.append(pid)
            if 'agotado' in disponibilidad and total == 0:
                disponibles_ids.append(pid)
        productos = productos.filter(id__in=disponibles_ids)

    # 6. IDs de variantes favoritas del usuario
    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = list(
            Favoritos.objects.filter(usuario=request.user)
            .values_list('talla_variante_id', flat=True)
        )

    # 7. Construir lista final
    productos_con_datos = []
    for producto in productos.distinct():
        variantes = TallaVariante.objects.filter(color_producto__producto=producto)
        agregados = variantes.aggregate(
            total_stock=Sum('stock'),
            precio_min=Min('precio'),
            precio_max=Max('precio')
        )
        var_fav = variantes.filter(stock__gt=0).first() or variantes.first()

        productos_con_datos.append({
            'producto': producto,
            'total_stock': agregados['total_stock'] or 0,
            'precio_min': agregados['precio_min'] or 0,
            'precio_max': agregados['precio_max'] or 0,
            'en_favoritos': var_fav and var_fav.id in favoritos_ids,
            'variante_id': var_fav.id if var_fav else None,
        })

    # 8. Render con contexto
    return render(request, 'catalogo.html', {
        'productos_con_datos': productos_con_datos,
        'favoritos_ids': favoritos_ids,
        'escuelas': Escuela.objects.all(),
        'categorias': Categoria.objects.all(),
        'tallas': Talla.objects.all(),
        'escuelas_seleccionadas': escuela_ids,
        'categorias_seleccionadas': categoria_ids,
        'tallas_seleccionadas': talla_ids,
        'disponibilidad_seleccionada': disponibilidad,
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

    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = list(
            Favoritos.objects
                .filter(usuario=request.user)
                .values_list('talla_variante_id', flat=True)
        )       

    contexto = {
        'producto': producto,
        'colores': colores,
        'color_tallas': color_tallas,
        'variantes_json': json.dumps(variantes_data, cls=DjangoJSONEncoder),
        # === inyectamos favoritos_ids ===
        'favoritos_ids': favoritos_ids,
    }

    return render(request, 'producto.html', contexto)

@login_required
def favoritos(request):
    # Traer las variantes favoritas con todas las relaciones necesarias
    favoritos_qs = (
        Favoritos.objects
        .filter(usuario=request.user)
        .select_related(
            'talla_variante__color_producto__producto',
            'talla_variante__talla',
            'talla_variante__color_producto__color'
        )
    )

    for f in favoritos_qs:
        f.total = f.cantidad * f.talla_variante.precio

    # En vez de solo variantes, pasa el queryset completo de Favoritos
    return render(request, 'favoritos.html', {
        'favoritos': favoritos_qs,
    })


def contacto(request):
    return render(request, 'contacto.html')

def login_required_json(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'No autenticado'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view   

@login_required_json
@require_POST
def toggle_favorito(request, variante_id):
    usuario = request.user
    try:
        variante = TallaVariante.objects.get(id=variante_id)
    except TallaVariante.DoesNotExist:
        return JsonResponse({'error': 'Variante no encontrada'}, status=404)
    
    cantidad = request.POST.get('cantidad')
    try:
        cantidad = int(cantidad)
        if cantidad < 1:
            cantidad = 1
    except (TypeError, ValueError):
        cantidad = 1  # valor por defecto si no se proporciona cantidad válida

    favorito, creado = Favoritos.objects.get_or_create(
        usuario=usuario,
        talla_variante=variante
    )

    if not creado:
        favorito.delete()
        estado = 'eliminado'
    else:
        favorito.cantidad = cantidad
        favorito.save()
        estado = 'agregado'

    return JsonResponse({'estado': estado})


@login_required
@require_POST
def actualizar_cantidad_favorito(request, variante_id):
    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad < 1:
        return JsonResponse({'error': 'Cantidad inválida'}, status=400)

    try:
        favorito = Favoritos.objects.get(usuario=request.user, talla_variante_id=variante_id)
        favorito.cantidad = cantidad
        favorito.save()
        return JsonResponse({'estado': 'ok', 'cantidad': favorito.cantidad})
    except Favoritos.DoesNotExist:
        return JsonResponse({'estado': 'no_agregado'})
