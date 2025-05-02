# usuarios/models.py

from django.contrib.auth.models import User
from django.db import models

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    es_administrador = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


