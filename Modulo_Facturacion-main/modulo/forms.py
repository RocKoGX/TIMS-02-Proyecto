from django import forms
from .models import Cliente, Empresa, Producto

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente  # Asegúrate de que está asociado al modelo correcto
        fields = ['dni', 'nombre', 'direccion', 'telefono', 'correo']  # Campos del formulario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'precio', 'stock']  # Campos del formulario

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['ruc', 'nombre', 'direccion', 'telefono', 'imagen']  # Campos del formulario
