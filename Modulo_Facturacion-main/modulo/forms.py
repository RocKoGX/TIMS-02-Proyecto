from django import forms
from .models import Cliente, Empresa, Producto

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni', 'nombre', 'direccion', 'telefono', 'correo']

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

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'precio', 'stock']

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio <= 0 or precio > 10000:
            raise forms.ValidationError("El precio debe ser mayor a 0 y razonable (máx. 10,000).")
        return precio

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
