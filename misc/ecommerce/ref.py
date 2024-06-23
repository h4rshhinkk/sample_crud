# from django.views import View
# from django.shortcuts import render, get_object_or_404, redirect
# from django.forms import modelformset_factory
# from web.forms.product import ProductForm, ProductMultipleImage
# from web.models import Product, ProductMedia

# class ProductCreate(View):
#     def get(self, request, *args, **kwargs):
#         ProductMediaFormSet = modelformset_factory(ProductMedia, form=ProductMultipleImage, extra=1)
#         form = ProductForm()
#         media_forms = ProductMediaFormSet(queryset=ProductMedia.objects.none())
#         context = {
#             'form': form,
#             'media_forms': media_forms,
#         }
#         return render(request, 'web/product/product_create.html', context)

#     def post(self, request, *args, **kwargs):
#         ProductMediaFormSet = modelformset_factory(ProductMedia, form=ProductMultipleImage, extra=1)
#         form = ProductForm(request.POST, request.FILES)
#         media_forms = ProductMediaFormSet(request.POST, request.FILES)
#         if form.is_valid() and media_forms.is_valid():
#             product = form.save()
#             media_instances = media_forms.save(commit=False)
#             for media in media_instances:
#                 media.product = product
#                 media.save()
#             return redirect('web:product')
#         else:
#             context = {
#                 'form': form,
#                 'media_forms': media_forms,
#             }
#             return render(request, 'web/product/product_create.html', context)

# class ProductUpdate(View):
#     def get(self, request, *args, **kwargs):
#         ProductMediaFormSet = modelformset_factory(ProductMedia, form=ProductMultipleImage, extra=1)
#         id = kwargs.get('pk', None)
#         product = get_object_or_404(Product, id=id)
#         form = ProductForm(instance=product)
#         media_forms = ProductMediaFormSet(queryset=ProductMedia.objects.filter(product=product))
#         context = {
#             'form': form,
#             'media_forms': media_forms,
#             'id': id
#         }
#         return render(request, 'web/product/product_create.html', context)

#     def post(self, request, *args, **kwargs):
#         ProductMediaFormSet = modelformset_factory(ProductMedia, form=ProductMultipleImage, extra=1)
#         id = kwargs.get('pk', None)
#         product = get_object_or_404(Product, id=id)
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         media_forms = ProductMediaFormSet(request.POST, request.FILES, queryset=ProductMedia.objects.filter(product=product))
#         if form.is_valid() and media_forms.is_valid():
#             form.save()
#             media_instances = media_forms.save(commit=False)
#             for media in media_instances:
#                 media.product = product
#                 media.save()
#             return redirect('web:product')
#         else:
#             context = {
#                 'form': form,
#                 'media_forms': media_forms,
#                 'id': id
#             }
#             return render(request, 'web/product/product_create.html', context)