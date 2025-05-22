import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import Cliente, Empresa, FacturaProducto, Producto, Factura  # Importar el modelo Cliente
from .forms import ClienteForm, EmpresaForm, ProductoForm  # Importar el formulario Cliente

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def facturacion_view(request):
    if request.method == 'POST':
        codigo_producto = request.POST.get('codigo_producto')
        dni_cliente = request.POST.get('dni')

        if codigo_producto:
            try:
                producto_seleccionado = Producto.objects.get(codigo=codigo_producto)
                producto_data = {
                    'nombre': producto_seleccionado.nombre,
                    'precio': str(producto_seleccionado.precio)
                }
                return JsonResponse(producto_data)
            except Producto.DoesNotExist:
                pass

        if dni_cliente:
            try:
                cliente = Cliente.objects.get(dni=dni_cliente)
                cliente_data = {
                    'nombre': cliente.nombre,
                    'direccion': cliente.direccion,
                    'telefono': cliente.telefono,
                    'correo': cliente.correo
                }
                return JsonResponse(cliente_data)
            except Cliente.DoesNotExist:
                pass

    empresa = Empresa.objects.first()  # Obtén la empresa desde la base de datos
    productos_disponibles = Producto.objects.all()  # Obtén todos los productos disponibles
    return render(request, 'facturacion.html', {'empresa': empresa, 'productos_disponibles': productos_disponibles})

def cliente_view(request):
    if request.method == 'POST':
        dni_cliente = request.POST.get('dni')
        if dni_cliente:
            try:
                cliente = Cliente.objects.get(dni=dni_cliente)
                cliente_data = {
                    'nombre': cliente.nombre,
                    'direccion': cliente.direccion,
                    'telefono': cliente.telefono,
                    'correo': cliente.correo
                }
                return JsonResponse(cliente_data)
            except Cliente.DoesNotExist:
                pass

    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

def productos_view(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            print("Producto guardado")
            return redirect('productos')
        else:
            print("Errores de validación:", form.errors)
    else:
        form = ProductoForm()

    # Obtener todos los productos para mostrar en la tabla
    productos = Producto.objects.all()

    return render(request, 'productos.html', {
        'form': form,  # El formulario para agregar nuevos productos
        'productos': productos,  # La lista de productos para mostrar en la tabla
    })

def facturas_view(request):
    if request.method == 'GET':
        facturas = Factura.objects.all()
        return render(request, 'facturas.html', {'facturas': facturas})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def detalle_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    datosFactura= FacturaProducto.objects.filter(factura=factura)
    datosProductos = []
    for dato in datosFactura:
        datosProductos.append({
            'nombre': dato.producto.nombre,
            'precio': dato.producto.precio,
            'cantidad': dato.cantidad,
            'subtotal': dato.subtotal
        })
    factura_data = {
        'id': factura.id,
        'cliente': factura.cliente.nombre,
        'fecha': factura.fecha,
        'subtotal': factura.subtotal,
        'igv': factura.igv,
        'total': factura.total
    }
    return render(request, 'detalle_factura.html', {'factura': factura_data,
                                                    'productos': datosProductos})

def busqueda_view(request):
    if request.method == 'POST':
        busqueda = request.POST.get('busqueda')
        if busqueda:
            productos = Producto.objects.filter(nombre__icontains=busqueda)
            return render(request, 'busqueda.html', {'productos': productos, 'busqueda': busqueda})
    return render(request, 'busqueda.html')
    

def empresa_view(request):
    empresa = Empresa.objects.first()

    if request.method == "POST":
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            empresa = form.save(commit=False)
            if 'imagen' in request.FILES:
                empresa.imagen = request.FILES['imagen']
            empresa.ruc = form.cleaned_data['ruc']  # Asegúrate de obtener el valor del campo 'ruc'
            empresa.nombre = form.cleaned_data['nombre']
            empresa.direccion = form.cleaned_data['direccion']
            empresa.telefono = form.cleaned_data['telefono']
            empresa.save()
            print("Empresa Guardada/Actualizada correctamente")
            return redirect('empresa')
        else:
            print("Errores de validación:", form.errors)
    else:
        form = EmpresaForm(instance=empresa)

    return render(request, 'empresa.html', {'form': form, 'empresa': empresa})



def clientes_view(request):
    if request.method == "POST":  # Cuando se envía el formulario
        form = ClienteForm(request.POST)
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guardar el cliente
            print("Cliente guardado")  # Confirmación de guardado
            return redirect('clientes')  # Redirigir a la misma vista
        else:
            print("Errores de validación:", form.errors)  # Mostrar errores de validación
    else:
        form = ClienteForm()  # Para solicitudes GET o si el formulario no es válido

    # Obtener todos los clientes para mostrar en la tabla
    clientes = Cliente.objects.all()

    return render(request, 'clientes.html', {
        'form': form,  # El formulario para agregar nuevos clientes
        'clientes': clientes,  # La lista de clientes para mostrar en la tabla
    })

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)  # Obtener el cliente por ID
    if request.method == "POST":  # Si se envía el formulario
        form = ClienteForm(request.POST, instance=cliente)  # Formulario pre-rellenado
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guardar cambios
            return redirect('clientes')  # Redirigir a la lista de clientes
    else:  # Si es GET, mostrar el formulario con datos existentes
        form = ClienteForm(instance=cliente)
        # Deshabilitar ciertos campos
        form.fields['dni'].widget.attrs['readonly'] = True
        form.fields['nombre'].widget.attrs['readonly'] = True

    # Añadir a los datos de contexto información adicional
    return render(request, 'clientes.html', {
        'form': form,  # Formulario para editar cliente
        'clientes': Cliente.objects.all(),  # Lista de clientes para mostrar
        'editar_cliente': True  # Bandera para mostrar botones adicionales
    })

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)  # Obtener el cliente o mostrar 404 si no se encuentra
    cliente.delete()  # Eliminar el cliente de la base de datos
    return redirect('clientes')  # Redirigir a la lista de clientes

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)

    # Obtener todos los productos para mostrar en la tabla
    productos = Producto.objects.all()

    return render(request, 'productos.html', {
        'form': form,
        'productos': productos,
        'editar_producto': True
    })

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('productos')

# def guardar_factura(request):
#     print("Ingreso a guardar_factura")
#     if request.method == 'POST':

#         # Obtener datos del cliente, productos y fecha
#         cliente_id = request.POST.get('datosFactura')
#         print(cliente_id)
#         #cliente_data = json.loads(request.POST.get('cliente')) if request.POST.get('cliente') else {}

#         productos_data = json.loads(request.POST.get('productos')) if request.POST.get('productos') else []
#         fecha = request.POST.get('fecha') if request.POST.get('fecha') else ''

#         # Guardar la factura en la base de datos
#         factura = Factura(cliente=cliente_data, fecha=fecha)
#         factura.save()

#         # Guardar los productos asociados a la factura
#         for producto_data in productos_data:
#             producto = Producto.objects.get(pk=producto_data['id'])
#             factura.productos.add(producto)

#         # Devolver el número de factura generado
#         numero_factura = factura.id
#         return JsonResponse({'numero_factura': numero_factura})
#     else:
#         return JsonResponse({'error': 'Método no permitido'})

@csrf_exempt
def guardar_factura(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        cliente_id = body_data.get('cliente').get('dni')
        subtotal = float(body_data.get('extraData').get('subtotal', 0))
        igv = float(body_data.get('extraData').get('impuesto_igv', 0))
        total = float(body_data.get('extraData').get('total_pagar', 0))

        # Validar montos
        if subtotal <= 0 or total <= 0:
            return JsonResponse({'error': 'Los montos de la factura deben ser mayores a 0.'}, status=400)

        try:
            cliente_data = Cliente.objects.get(dni=cliente_id)
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

        factura = Factura(cliente=cliente_data, subtotal=subtotal, igv=igv, total=total)
        factura.save()

        for producto_data in body_data.get('productos'):
            producto = Producto.objects.get(codigo=producto_data.get('codigo'))
            cantidad = int(producto_data.get('cantidad'))
            subtotal_producto = float(producto_data.get('subtotal'))

            if cantidad <= 0 or subtotal_producto <= 0:
                return JsonResponse({'error': 'Cantidad o subtotal inválido en los productos'}, status=400)

            FacturaProducto.objects.create(
                factura=factura,
                producto=producto,
                cantidad=cantidad,
                subtotal=subtotal_producto
            )

        return JsonResponse({'numero_factura': factura.id})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
