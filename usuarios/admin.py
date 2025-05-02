# usuarios/admin.py
from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'direccion', 'telefono', 'es_administrador']
    search_fields = ['user__username', 'user__email']

admin.site.register(Usuario, UsuarioAdmin)
