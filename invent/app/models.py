from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone



# Modelo de Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

# Modelo de Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

# Modelo de Producto
class Producto(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(blank=True, max_length=255)
    update_user = models.CharField(blank=True, max_length=255)
    stock_minimo = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)


    def __str__(self):
        return self.nombre


# Modelo de Movimiento de Producto
class MovimientoProducto(models.Model):
    TIPO_MOVIMIENTO = [
        ('COMPRA', 'Compra'),
        ('VENTA', 'Venta'),
        ('AJUSTE_ENTRADA', 'Ajuste Entrada'),
        ('AJUSTE_SALIDA', 'Ajuste Salida'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.stock_producto.producto.nombre} - {self.cantidad}"

    def save(self, *args, **kwargs):
        if self.tipo in ['COMPRA', 'AJUSTE_ENTRADA']:
            self.stock_producto.stock += self.cantidad
        elif self.tipo in ['VENTA', 'AJUSTE_SALIDA']:
            self.stock_producto.stock -= self.cantidad
        self.stock_producto.save()
        super().save(*args, **kwargs)

# Modelo de Documento (Factura, Boleta, Orden de Compra)
class Documento(models.Model):
    TIPO_DOCUMENTO = [
        ('FACTURA', 'Factura'),
        ('BOLETA', 'Boleta'),
        ('ORDEN_COMPRA', 'Orden de Compra'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_DOCUMENTO)
    numero = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.tipo} #{self.numero}"

# Modelo de Detalle de Documento
class DetalleDocumento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.producto.producto.nombre} - {self.cantidad} unidades en {self.producto.nombre}"
