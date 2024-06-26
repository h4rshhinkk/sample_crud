# class RegionForm(forms.ModelForm):
#     name = forms.CharField(
#         label="Name", max_length=225, required = True,
#         widget=forms.TextInput( attrs={'class': 'form-control effect input-text'} ),
#         error_messages={ 'required': 'The name should not be empty' }
#     )
#     country = CountryChoiceField(
#             required=True,
#             queryset=Countries.objects.filter(is_active = True),
#             empty_label='Select a country',
#             widget=forms.Select(attrs={'class': 'form-control input-select'}),
#             error_messages={'required': 'The country should not be empty'})

#     class Meta:
#         model = Region
#         fields = ['name','country']
#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get('name')
#         country = cleaned_data.get('country')
#         if Region.objects.filter(~Q(pk=self.instance.pk),name__iexact=name,country=country ,is_active=True).exists():
#             self.add_error('name',"Region with this name already exists in selected country.")
#         return cleaned_data



