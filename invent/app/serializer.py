from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["codigo", "nombre", "descripcion", "precio_venta", "precio_compra",
            "activo", "stock_minimo", "stock"]
        # fields = '__all__'