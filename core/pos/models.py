from django.db import models
import datetime

# modelos para cada tabla de la base de datos

#clase de categorias de productos
# relacionada ManytoMany a Producto en campo Producto.categoria
class CategoriasProductos(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.CharField(max_length=200)

#clase de productos
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    unidad = models.CharField(max_length=20)
    imagen = models.CharField( max_length=50)
    costo = models.FloatField()
    precio_detal = models.FloatField()
    precio_mayor = models.FloatField()
    precio_especial = models.FloatField()
    categoria = models.ManyToManyField(CategoriasProductos)

#clase de relacion entre pedidos y sus productos con sus cantidades y precio a considerar
class ProductosPedido(models.Model):
    producto = models.IntegerField()
    cantidad = models.IntegerField()
    precio = models.FloatField()



#clase de pedidos
class Pedido(models.Model):
    
    productos = models.ManyToManyField(ProductosPedido)
    status = models.CharField(max_length=50)
    precio_total = models.FloatField()

