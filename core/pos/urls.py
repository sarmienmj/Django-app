from django.urls import path
from .views import *

app_name="pos"

urlpatterns = [
    path('',  PosView.as_view(), name='pos'),
    path('filtrar-categorias/', FiltrarCategorias.as_view(), name='filtrarCategorias'),
    path('guardar-pedido/', guardarPedidoPost.as_view(), name='guardarPedido'),
    path('pedidosList/', PedidosList.as_view(), name='listaPedidos'),
]
