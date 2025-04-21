from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    es_administrador = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado')
    ])

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Favoritos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

class DetallesPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

class HistorialStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad_anterior = models.PositiveIntegerField()
    cantidad_nueva = models.PositiveIntegerField()

class ClicksWhatsapp(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)