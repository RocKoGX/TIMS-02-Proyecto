from django import forms
from .models import Cliente, Empresa, Producto
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni', 'nombre', 'direccion', 'telefono', 'correo']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio.")
        if len(nombre) > 100:
            raise forms.ValidationError("El nombre no puede superar 100 caracteres.")
        return nombre

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError("El DNI debe tener exactamente 8 dígitos numéricos.")
        return dni

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if telefono and (not telefono.isdigit() or len(telefono) != 9):
            raise forms.ValidationError("El teléfono debe tener exactamente 9 dígitos numéricos.")
        return telefono
    
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo:
            # Usa validator o regex simple
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
                raise forms.ValidationError("Ingrese un correo electrónico válido.")
        return correo


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'precio', 'stock']

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio <= 0 or precio > 10000:
            raise forms.ValidationError("El precio debe ser mayor a 0 y razonable (máx. 10,000).")
        return precio
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if not re.match(r'^\d+$', codigo):
            raise forms.ValidationError("El código del producto debe contener solo números.")
        return codigo

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock <= 0 or stock > 1000:
            raise forms.ValidationError("El stock debe ser mayor a 0 y razonable (máx. 1000 unidades).")
        return stock

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['ruc', 'nombre', 'direccion', 'telefono', 'imagen']

    def clean_ruc(self):
        ruc = self.cleaned_data['ruc']
        if not ruc.isdigit() or len(ruc) != 11:
            raise forms.ValidationError("El RUC debe contener exactamente 11 dígitos.")
        return ruc

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if telefono and (not telefono.isdigit() or len(telefono) != 9):
            raise forms.ValidationError("El teléfono debe contener exactamente 9 dígitos.")
        return telefono
