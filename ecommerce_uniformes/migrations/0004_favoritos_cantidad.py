# Generated by Django 5.2 on 2025-05-23 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_uniformes', '0003_remove_favoritos_producto_favoritos_talla_variante'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritos',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
