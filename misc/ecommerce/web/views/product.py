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


class ProductView(View):
    def get(self, request, *args, **kwargs):
        context, response = {}, {}
        page = int(request.GET.get('page', 1))
        products = Product.objects.filter(is_active=True)
        paginator = Paginator(products, PAGINATION_PERPAGE)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

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

    def post(self,request, *args, **kwargs):
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.save()
            print('data',data)
            response={
                'status':True,
                'message': 'Form submitted successfully!',
            }
        else:
                print('--invalid---')
                print('form',form.errors)
                response = {
                    'status': False,
                    'form_errors': form.errors,
                    'message': 'Form Submission Failed!',
                }
        return redirect('web:product')   
     
class ProductUpdate(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        data = {}
        obj = get_object_or_404(Product, id = id)
        form = ProductForm(instance=obj)
        context = {'form': form, 'id': id}
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