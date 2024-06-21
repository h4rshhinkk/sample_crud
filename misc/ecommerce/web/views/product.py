from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from web.forms.product import ProductForm
from web.helper import renderfile, is_ajax, LogUserActivity
from web.models import Category,Product
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import *
from web.constantvariables import PAGINATION_PERPAGE
from django.shortcuts import get_object_or_404
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
        data = {}
        form = ProductForm()
        context = {'form': form, 'id': 0}
        data['status'] = True
        data['title'] = 'Create Productz'
        data['template'] = render_to_string('web/product/product_form.html', context, request=request)
        return JsonResponse(data)
