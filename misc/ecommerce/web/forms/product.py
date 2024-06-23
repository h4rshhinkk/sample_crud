from django import forms
from web.models import Category,Product,ProductMedia
from django.forms import inlineformset_factory


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

class ProductMultipleImage(forms.ModelForm):
    class Meta:
            model = ProductMedia    
            fields = ['image','is_default']
            widgets = {
                'image': forms.FileInput(attrs={'class': 'form-control','required':'True'}),
                'is_default': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            }


MultipleImageInputFormFormSet = inlineformset_factory(
    Product,
    ProductMedia,
    form=ProductMultipleImage,
    extra=2,
    can_delete=True,
)