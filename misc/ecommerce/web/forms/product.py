from django import forms
from web.models import Category,Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','name','description','price']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control','required':'True'}),
            'name': forms.TextInput(attrs={'class': 'form-control','required':'True'}),
            'description': forms.Textarea(attrs={'class': 'form-control','required':'True'}),
            'price': forms.NumberInput(attrs={'class': 'form-control','required':'True'}),
            
        }