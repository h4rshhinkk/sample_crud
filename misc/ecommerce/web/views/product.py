from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from django.urls import reverse
from web.forms.product import *
from web.helper import renderfile, is_ajax, LogUserActivity
from web.models import Category,Product
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import *
from web.constantvariables import PAGINATION_PERPAGE
from django.shortcuts import get_object_or_404,render,redirect
from django.db import transaction
from django.db.models import Q

class ProductView(View):
    def get(self, request, *args, **kwargs):
        context, response = {}, {}
        page = int(request.GET.get('page', 1))
        search_query = request.GET.get('search', '')
        if search_query:
            products = Product.objects.filter(
                name__icontains=search_query,
                is_active=True
            )
        else:
            products = Product.objects.filter(is_active=True)
        
        
        context['products'], context['current_page'] = products, page
        if is_ajax(request=request):
            response['status'] = True
            response['pagination'] = render_to_string("web/product/pagination.html",context=context,request=request)
            response['template'] = render_to_string('web/product/product_list.html', context, request=request)
            return JsonResponse(response)
        context['form']  = ProductForm()
        return renderfile(request, 'product', 'index', context)
    
class ProductCreate(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': ProductForm(),
            'item_formset': MultipleImageInputFormFormSet()
        }
        return render(request, 'web/product/product_create.html', context)

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        formset = MultipleImageInputFormFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product_instance = form.save()

            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product_instance
                instance.save()
            response = {
                'status': True,
                'message': 'Form submitted successfully!',
            }
            return redirect('web:product')
        else:
            print('--invalid---')
            print('form errors:', form.errors)
            print('formset errors:', formset.errors)
            response = {
                'status': False,
                'form_errors': form.errors,
                'formset_errors': formset.errors,
                'message': 'Form Submission Failed!',
            }
            
            context = {
                'form': form,
                'item_formset': formset
            }
            return render(request, 'web/product/product_create.html', context)

class ProductDelete(View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        response = {}
        obj = get_object_or_404(Product, id = id)
        obj.delete()
        
        response['status'] = True
        response['message'] = "Product deleted successfully"
        return JsonResponse(response)


class ProductUpdate(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        data = {}
        obj = get_object_or_404(Product, id = id)
        form = ProductForm(instance=obj)
        item_formset = MultipleImageInputFormFormSet(instance=obj)
        context = {'form': form, 'id': id,'item_formset':item_formset}
        data['status'] = True
        data['title'] = 'Edit Product'
        return render(request, 'web/product/product_create.html', context)
    
    def post(self, request, *args, **kwargs):
        data, response = {} , {}
        id = kwargs.get('pk', None)
        obj = get_object_or_404(Product, id=id)
        form = ProductForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            response['message'] = "Product updated successfully"
            return redirect('web:product')
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Edit Product'
            response['valid_form'] = False
            print('form',form.errors)
            return render(request, 'web/product/product_create.html', context)
        

class ProductImageView(View):
    def get(self, request, *args, **kwargs):
        products = ProductMedia.objects.all()
        print("products",products)
        context = {'products_images': products}
        return render(request, 'web/product/product_image_list.html', context)
    

def search(request):
    query = request.GET.get('search', '')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(keyword__icontains=query)
        ).distinct()
    else:
        products = Product.objects.all()

    return render(request, 'web/product/search.html', {'products': products})


class ProductVariantView(View):
    def get(self, request, *args, **kwargs):
        context, response = {}, {}
        page = int(request.GET.get('page', 1))
        prod_variants = Variants.objects.all()
        context['current_page'] =  page
        context = {'prod_variants': prod_variants}
        if is_ajax(request=request):
            response['status'] = True
            response['pagination'] = render_to_string("web/product/pagination.html",context=context,request=request)
            response['template'] = render_to_string('web/product/product_variant_list.html', context, request=request)
            return JsonResponse(response)
        return render(request, 'web/product/product_variant_index.html', context)
    
class ProductVariantCreate(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': ProductVariantForm(),
            'id': 0
        }
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'html_form': render_to_string('web/product/product_variant_form.html', context, request=request)})
        return render(request, 'web/product/product_variant_form.html', context)
    
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
            form = ProductVariantForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.save()
                response = {
                    'status': True,
                    'message': 'Form submitted successfully!',
                }
            else:
                response = {
                    'status': False,
                    'form_errors': form.errors,
                    'message': 'Form Submission Failed!',
                }
            return JsonResponse(response)
        return redirect('web:product_variant')