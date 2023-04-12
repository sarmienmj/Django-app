from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View, ListView
from django.core import serializers
from .models import Producto,CategoriasProductos, Pedido, ProductosPedido

#Vista 1 de sistema pos
class PosView(View):
    

    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()
        categorias = CategoriasProductos.objects.all()
        context={
            "productos":productos,
            "categorias":categorias,
        }
        return render(request, 'pos.html', context)

class FiltrarCategorias(View):

    def post(self,request,*args, **kwargs):
        categoria_id = (request.POST['categoria'])
        qs = Producto.objects.filter(categoria=categoria_id)
        productos=[]
        for producto in qs:
            p = {
                'id':producto.pk,
                'nombre':producto.nombre,
                'precio':producto.precio_detal,
                'imagen':producto.imagen,
                'unidad':producto.unidad,
            }
            productos.append(p)
        return JsonResponse(productos,safe=False)
    
class guardarPedidoPost(View):
    def post(self,request,*args, **kwargs):
        pedido = request.POST
        pedido = pedido.copy()
        precio_total = pedido.popitem()
        pedido_dict = pedido.dict()
        precio_total = precio_total[1][0]
        pedido_nuevo = Pedido(status='creado', precio_total=precio_total)
        pedido_nuevo.save()

        rango = int((len(pedido_dict) / 5))

        for x in range(0,rango):
            id = pedido_dict['pedido[%i][id]' % x]
            cantidad = float(pedido_dict['pedido[%i][cantidad]' % x])
            precio = float(pedido_dict['pedido[%i][precio]' % x])
            productoDePedido = ProductosPedido(producto=id,cantidad=cantidad,precio=precio)
            productoDePedido.save()
            pedido_nuevo.productos.add(productoDePedido)

        pedido_nuevo.save()
        return HttpResponse(200, content_type='text/plain')

class PedidosList(View):
    
    def post(self,request,*args, **kwargs):
        pedidos = Pedido.objects.all().order_by('-pk')
        pedidos_lista = []
        for pedido in pedidos:
            p = {
                "pk": pedido.pk,
                "status": pedido.status,
                "preciototal": pedido.precio_total,
            }
            pedidos_lista.append(p)
        return JsonResponse(pedidos_lista,safe=False)

    