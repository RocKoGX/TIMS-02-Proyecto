from django.db import models

class Cliente(models.Model):
    dni = models.CharField(max_length=8, unique=True)  # Identificador único
    nombre = models.CharField(max_length=100)  # Nombre del cliente
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Dirección (opcional)
    telefono = models.CharField(max_length=9, blank=True, null=True)  # Teléfono (opcional)
    correo = models.EmailField(blank=True, null=True)  # Correo electrónico (opcional)

    def __str__(self):
        return f"{self.nombre} ({self.dni})"

class Producto(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # Código único
    nombre = models.CharField(max_length=100)  # Nombre del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    stock = models.PositiveIntegerField()  # Cantidad en stock

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

class Empresa(models.Model):
    ruc = models.CharField(max_length=11)  # Identificador único
    nombre = models.CharField(max_length=100)  # Nombre de la empresa
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Dirección (opcional)
    telefono = models.CharField(max_length=9, blank=True, null=True)  # Teléfono (opcional)
    imagen = models.ImageField(upload_to='empresas/', blank=True, null=True)  # Imagen de la empresa (opcional)


    def __str__(self):
        return f"{self.nombre} ({self.ruc})"
    


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)  # Campo para la fecha de la factura
    #numero_factura = models.CharField(max_length=20, unique=True)  # Campo para el número de factura
    productos = models.ManyToManyField(Producto, through='FacturaProducto')
    igv = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Campo para el IGV de la factura
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Campo para el subtotal de la factura
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Campo para el total de la factura

    def __str__(self):
        return f"Factura #{self.numero_factura} - {self.cliente.nombre}"

class FacturaProducto(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()  # Cantidad de productos
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Subtotal por producto