var pedido = []
var bcv = 24.23

var n = ""

 function numerosTeclado(){
    return new Promise((resolve, reject) =>{
        $(".boton-calculadora").unbind()
        $(".boton-calculadora").click(function(){
            boton = $("#" + this.id)
            if (boton.text() === "Enter"){
                resolve(n)
            }
            if (boton.text() === ","){
                n = n + "."
            }
            else{
                if (n == ''){
                    n = boton.text()
                }
                else {
                    n = String(n) + boton.text()
                }
            }   
        })
    })
}

$(document).ready(function () {
    
    const capitalize = str => str.charAt(0).toUpperCase() + str.slice(1);
    cambiarPrecioTotal();

    $(".agregar-producto-pedido").on('click', function (){
        texto = $("#"+ this.id + "> p").text()
        productoInfo = texto.split('-')
        let productoid = parseInt(productoInfo[0])

        if(revisarExisteProductoPedido(productoid) == "si"){
            cambiarPrecioProductoPedido(productoid)
        }
        else {
            let nombre = productoInfo[1]
            let precio = parseFloat(productoInfo[2]).toFixed(2)
            let precioBs = (precio * bcv).toFixed(2)
            let unidad = productoInfo[3]
            let cantidad = 1
            pedidodiv = `<div id="${productoid}" class="container apuntar mt-1 border pedido-div-producto"><div class="row"><div class="col-6"><h5 class="">${capitalize(nombre)}</h5><p class="fs-6">1 kilos en ${precio}$/${unidad}</p></div><div class="col-6"><h6>${precio}$ // ${precioBs}Bs.F</h6></div></div></div>`
            $("#lista-de-pedidos").append(pedidodiv)
            pedido.push({id:productoid, nombre:nombre, precio:precio, unidad:unidad, cantidad:cantidad})
            addEvent(productoid)
            cambiarPrecioTotal()
        }
    })

    function addEvent(productoid){
        
        cambiarPrecioProductoPedido(productoid)

        $(".pedido-div-producto").unbind();
        $(".pedido-div-producto").on('click', function(){
            id = this.id;
            cambiarPrecioProductoPedido(id)

        })
    }

    function cambiarPrecioProductoPedido(id){
        p_div_producto = $("#"+ id + "> div > div > p").text();
        $(".pedido-div-producto").css('background-color', '#fff')
        $("#"+ id).css('background-color', '#C7D4B6')

            $("#boton-borrar").on('click', function(){
                for(let i in pedido) {
                    // Comparar nombre
                    if(pedido[i].id == id) {
                        console.log(pedido[i].id, id)
                        // Se encontró, guardar posición y salir del ciclo
                        found = i;
                        break;
                    }
                }
                // Si el elemento existe, found será igual o mayor que cero
                if(found > -1) {
                    // Eliminar elemento del arreglo
                    pedido.splice(found, 1);
                    cambiarPrecioTotal()
                    $("#"+ id).remove()
                    return 0
                }
            })

            var x =  numerosTeclado().then((result) => {
                $("#"+ id).css('background-color', '#fff')
                return result
            });

            const asignarCantidad = async () => {
                const a = await x;

                pedido.forEach(producto => {
                    if(producto.id == id){
                        cantidad = parseFloat(a).toFixed(2)
                        producto.cantidad = cantidad;
                        $("#"+ id + "> div > div > p").text(`${cantidad} ${producto.unidad} en ${producto.precio}$/${producto.unidad}`);

                        precio = (cantidad * producto.precio).toFixed(2)
                        precioBs = (precio * bcv).toFixed(2)
                        $("#"+ id + "> div > div > h6").text(`${precio}$ // ${precioBs}Bs.F`)
                    }
                    
                });
                cambiarPrecioTotal()
            };
        asignarCantidad();
        n=''
        
    }

    function cambiarPrecioTotal(total){
        if (total != 0){
            let precioTotal = 0.00
            let precioTotalBs = 0.00
            $("#precio-total").text(`Total: ${precioTotal.toFixed(2)}$ // ${precioTotalBs}Bs.F`)
        }
        let precioTotal = 0
        let precioTotalBs = 0
        pedido.forEach(p => {
            precioTotal = precioTotal + (p.precio * p.cantidad)
        })
        precioTotalBs = (precioTotal * bcv).toFixed(2)
        $("#precio-total").text(`Total: ${precioTotal.toFixed(2)}$ // ${precioTotalBs}Bs.F`)
    }

    $(".filtrar-por-categoria").on('click', function(){
        var textoCategoria = $("#"+ this.id + "> p").text()
        var categoriaInfo = textoCategoria.split('-')
        var categoriaId = categoriaInfo[0]

        $.ajax({url: 'filtrar-categorias/', data : {'categoria':categoriaId,}, type: 'POST', dataType:'json',
            success: function (response){
                $("#divProductos").html("")
                response.forEach(producto => {
                    productoDiv = `<div class="p-2 bg-white apuntar text-center border rounded agregar-producto-pedido" id="producto-div-${producto.id}" style="width: 180px; height: 150px;" ><p style="display: none;">${producto.id}-${producto.nombre}-${producto.precio}-${producto.unidad}</p><div class="overflow-hidden p-2 text-center" style="width: 100px; height: 100px;"><img src="${producto.imagen}" class="img-fluid rounded-top " alt="" style="width: 200px;"></div><ul class="list-inline"><li class="list-inline-item text-capitalize"><p class="fw-semibold fs-6">${producto.nombre}</p></li><li class="list-inline-item text-capitalize"><p class="fs-6 fw-light">${producto.precio}$/${producto.unidad}</p></li></ul></div>`
                    $("#divProductos").append(productoDiv)
                    $(".agregar-producto-pedido").unbind()
                    $(".agregar-producto-pedido").on('click', function (){
                        texto = $("#"+ this.id + "> p").text()
                        productoInfo = texto.split('-')
                        let productoid = parseInt(productoInfo[0])
                
                        if(revisarExisteProductoPedido(productoid) == "si"){
                            cambiarPrecioProductoPedido(productoid)
                        }
                        else {
                            let nombre = productoInfo[1]
                            let precio = parseFloat(productoInfo[2]).toFixed(2)
                            let precioBs = (precio * bcv).toFixed(2)
                            let unidad = productoInfo[3]
                            let cantidad = 1
                            pedidodiv = `<div id="${productoid}" class="container apuntar mt-1 border pedido-div-producto"><div class="row"><div class="col-6"><h5 class="">${capitalize(nombre)}</h5><p class="fs-6">1 kilos en ${precio}$/${unidad}</p></div><div class="col-6"><h6>${precio}$ // ${precioBs}Bs.F</h6></div></div></div>`
                            $("#lista-de-pedidos").append(pedidodiv)
                            pedido.push({id:productoid, nombre:nombre, precio:precio, unidad:unidad, cantidad:cantidad})
                            addEvent(productoid)
                            cambiarPrecioTotal()
                        }
                    })
                })
            },
        })
    })

    function revisarExisteProductoPedido(id){
        var f = "no"
        pedido.forEach(p => {
            if (p.id == id){
                f = "si"
            }
        })
        return f 
    }

    $("#botonGuardarPedido").on('click', function () {
        var precioT = 0
        pedido.forEach(p => {precioT = precioT + (p.precio * p.cantidad)})
        $.ajax({url:"guardar-pedido/", data:{'pedido':pedido, 'precioT':precioT}, type:'POST',
            success: function(response){
                    pedido = []
                    $("#lista-de-pedidos").html("")
                    cambiarPrecioTotal(0)
                }
        })
    })

    $("#boton-listar-pedidos").on('click', function (){
        $("#lista-pedidos-div").css("display", "block")
        $("#hr-ocultar").hide()
        $.ajax({
            type: "POST",
            url: "pedidosList/",
            dataType: "json",
            success: function (response) {
                response.forEach(ped =>{
                    pedidoFiltradosDiv = 
                    `<tr>
                        <th>{ped.fecha}</th>
                        <td>${ped.pk}</td>
                        <td>{ped.cliente}</td>
                        <td>{ped.cajero}</td>
                        <td>${ped.preciototal}</td>
                        <td>${ped.status}</td>
                    </tr>`
                    $("#tabla-pedidos").append(pedidoFiltradosDiv)
                })

            }
        });
        $("#boton-listar-pedidos").unbind()
    })
    $("#cerrar-listado-pedidos").on('click', function(){
        $("#hr-ocultar").show()
        $("#lista-pedidos-div").css("display", "none")
        $("#tabla-pedidos").html('<tr><th scope="row">pedido.fecha</th><td>pedido.id</td><td>pedido.Cliente</td><td>pedido.cajero</td><td>pedido.total</td><td>pedido.status</td></tr>')
    })

    $( function() {
        var availableTags = ["Scheme"];
        $( "#buscar-productos" ).autocomplete({
          source: availableTags
        });
      } );
});