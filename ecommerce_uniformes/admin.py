from django.contrib import admin
from .models import Usuario, Pedido, Producto, Favoritos, DetallesPedido, HistorialStock, ClicksWhatsapp

# Registra los modelos para que sean visibles en el panel de administración
admin.site.register(Usuario)
admin.site.register(Pedido)
admin.site.register(Producto)
admin.site.register(Favoritos)
admin.site.register(DetallesPedido)
admin.site.register(HistorialStock)
admin.site.register(ClicksWhatsapp)