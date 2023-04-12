from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.core import serializers
from .models import Producto,CategoriasProductos, Pedido, ProductosPedido

###Vista principal del sistema POS
class PosView(View):
    
    ###Request Get Busca todos los productos y categorias y las envia al Front
    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()
        categorias = CategoriasProductos.objects.all()
        context={
            "productos":productos,
            "categorias":categorias,
        }
        return render(request, 'pos.html', context)

### Vista para filtrar por los productos por categorias
### Desde el front se hace una peticion POST a la url 'pos/filtrar-categorias/'
### El front envia un numero en la peticion POST que es igual al numero de categoria que se quiere filtrar
class FiltrarCategorias(View):

    ### peticion POST
    def post(self,request,*args, **kwargs):
        # Numero de categoria recibida en la peticion
        categoria_id = (request.POST['categoria'])

        # Si categoria_id es 0 buscar todos los productos
        # Se usa para reiniciar los filtros
        if categoria_id == "0":
            # Query de todos los productos
            #Devuelve QuerySet
            qs = Producto.objects.filter()

        # Si no es 0 busca filtra los productos por el ID que envia el FRONT 
        else:
            # Query de buscar todos los productos que tengan esta categoria 'categoria_id'
            #devuelve QuerySet
            qs = Producto.objects.filter(categoria=categoria_id)

        #iniciar lista que se enviara al front con los productos filtrados
        productos=[]

        # Ciclo for usado para llevar los datos de un QuerySet qs a un dict llamado Productos
        # No se puede enviar un queryset como en formato Json por eso aca se lleva a Dict
        for producto in qs:
            #por cada producto en el queryset separarlos y hacerles append() a el dict Productos
            p = {
                'id':producto.pk,
                'nombre':producto.nombre,
                'precio':producto.precio_detal,
                'imagen':producto.imagen,
                'unidad':producto.unidad,
            }
            productos.append(p)

        # enviar el dict en formato Json para el front
        return JsonResponse(productos,safe=False)

### Vista que guarda los pedidos recibidos desde el front en peticion POST
### El front envia un array de productos y el precio total del pedido en USD$ a la url 'pos/guardar-pedido/'
class guardarPedidoPost(View):

    # definir la peticion POST
    def post(self,request,*args, **kwargs):
        #Recibir el pedido desde la peticion
        #se recibe un dato de tipo QueryDict que es inmutable
        pedido = request.POST
        #hacemos una copia mutable de 'pedido' para trabajar con ella
        pedido = pedido.copy()
        #En el pedido el precio total se ingresa de ultimo en el Dict, para obtenerlo usamos popitem() que saca el ultimo elemento del Dict
        precio_total = pedido.popitem()
        #llevamos pedido de tipo de dato QueryDict a Dict para trabajarlo mejor
        pedido_dict = pedido.dict()

        # Extraemos el valor del precio total del dict que creamos con .popitem()
        precio_total = precio_total[1][0]

        #creamos el pedido en la variable pedido_nuevo, status inicial 'creado' y asignamos el precio total
        pedido_nuevo = Pedido(status='creado', precio_total=precio_total)
        #guardamos este pedido_nuevo en la BD
        pedido_nuevo.save()
        
        ### Añadir los productos, cantidad y precio al pedido

        #rango es una variable que usamos para recorrer el dict del pedido_dict de donde extraeremos los productos para agregarlos a pedido_nuevo
        rango = int((len(pedido_dict) / 5))

        #Ciclo for para recorrer cada producto del pedido y obtener sus datos
        for x in range(0,rango):
            id = pedido_dict['pedido[%i][id]' % x]
            cantidad = float(pedido_dict['pedido[%i][cantidad]' % x])
            precio = float(pedido_dict['pedido[%i][precio]' % x])

            # Guardamos los productos del pedido en la bd
            productoDePedido = ProductosPedido(producto=id,cantidad=cantidad,precio=precio)
            productoDePedido.save()
            # asignamos los productos a pedido_nuevo
            pedido_nuevo.productos.add(productoDePedido)

        #guardamos el pedido con todos sus productos asignados y su precio total
        pedido_nuevo.save()
        #respuesta de la peticion post al front
        return HttpResponse(200, content_type='text/plain')

### Vista para listar los pedidos 
# Al momento de listar los pedidos el front hace una peticion POST a la ruta 'pos/pedidosList/'
class PedidosList(View):
    
    def post(self,request,*args, **kwargs):
        # pedidoses un QuerySet y hace un query a la base de datos de todos los pedidos en orden descendente ordenados por su Id o pk (pk: Primary Key)
        pedidos = Pedido.objects.all().order_by('-pk')
        # pedidos_lista es un dict que enviaremos al front con todos pedidos, no podemos enviar un dato QuerySet al front
        pedidos_lista = []
        #recorremos cada pedido en el QuerySet Pedidos para añadirlo al dict 'pedidos_lista'
        for pedido in pedidos:
            p = {
                "pk": pedido.pk,
                "status": pedido.status,
                "preciototal": pedido.precio_total,
            }
            pedidos_lista.append(p)
        #enviamos dict de pedidos al front
        return JsonResponse(pedidos_lista,safe=False)

    