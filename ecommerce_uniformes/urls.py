
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('usuarios/', include('usuarios.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('producto/<int:id>', views.producto, name='producto'),
    path('contacto/', views.contacto, name='contacto'),
    path('toggle-favorito/<int:variante_id>/', views.toggle_favorito, name='toggle-favorito'),
    path('actualizar-cantidad-favorito/<int:variante_id>/', views.actualizar_cantidad_favorito, name='actualizar_cantidad_favorito'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)