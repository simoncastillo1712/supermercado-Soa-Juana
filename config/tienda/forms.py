from django import forms
from .models import Categoria, Producto, Cliente, Proveedor

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [
            'nombre',
            'descripcion'
        ]

        labels = {
            'nombre': 'Nombre de la categoria: ',
            'descripcion': 'Descripción: '
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':3})
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'precio',
            'stock',
            'id_categoria'
        ]
        
        labels = {
            'nombre': 'Nombre del Producto: ',
            'precio': 'Precio: ',
            'stock' : 'Stock: ',
            'id_categoria' : 'Categoria'
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'id_categoria': forms.Select(attrs={'class': 'form-control'})
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'rut_cliente',
            'razon_social',
            'direccion',
            'telefono',
            'email'            
        ]
        
        labels ={
            'rut_cliente': 'Rut: ',
            'razon_social':'Nombre o Razón Social: ',
            'direccion':'Dirección: ',
            'telefono' : 'Teléfono: ',
            'email':'Correo Electronico'             
        }
        
        widgets = {
            'rut_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),            
        }
        
    def clean_rut_cliente(self):
        rut = self.cleaned_data['rut_cliente']
        if len(rut) < 8:
            raise forms.ValidationError(
                'El Rut NO ES válido.')
        return rut
            
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
                'rut_proveedor',
                'nombre_proveedor',
                'direccion',
                'telefono',
                'email',          
            ]
            
        labels ={
            'rut_proveedor': 'Rut Proveedor: ',
            'nombre_proveedor':'Razón Social: ',
            'direccion':'Dirección: ',
            'telefono' : 'Teléfono: ',
            'email':'Correo Electronico'             
        }
        
        widgets = {
            'rut_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),            
        }
    def clean_rut_proveedor(self):
        rut = self.cleaned_data['rut_proveedor']
        if len(rut) < 8:
            raise forms.ValidationError(
                'El Rut NO ES válido.')
        return rut