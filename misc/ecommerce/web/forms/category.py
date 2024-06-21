from django import forms
from web.models import Category

class CategoryForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',max_length=150,required=True,
        widget=forms.TextInput(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'The title should not be empty' }
    )

    description = forms.CharField(label='Description',max_length=150,required=True,widget=forms.Textarea(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'The Description should not be empty' })
    
    class Meta:
        model = Category
        fields = ['title','description']