from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from web.forms.category import CategoryForm
from web.helper import renderfile, is_ajax, LogUserActivity
from web.models import Category
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import *
from web.constantvariables import PAGINATION_PERPAGE
from django.shortcuts import get_object_or_404
from django.db import transaction
import json

class CategoryView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        context, response = {}, {}
        page = int(request.GET.get('page', 1))
        categories = Category.objects.all()

        paginator = Paginator(categories, PAGINATION_PERPAGE)
        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)

        context['categories'], context['current_page'] = categories, page
        if is_ajax(request=request):
            response['status'] = True
            response['pagination'] = render_to_string("web/category/pagination.html",context=context,request=request)
            response['template'] = render_to_string('web/category/category_list.html', context, request=request)
            return JsonResponse(response)
        context['form']  = CategoryForm()
        return renderfile(request, 'category', 'index', context)
    
class CategoryCreate(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = CategoryForm()
        print(form)
        context = {'form': form, 'id': 0}
        
        data['status'] = True
        data['title'] = 'Create Categoryy'
        data['template'] = render_to_string('web/category/category_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        response = {}
        form = CategoryForm(request.POST or None)
        if form.is_valid():
                with transaction.atomic():
                    title = request.POST.get('title', None)
                    description = request.POST.get('description', None)
                    if not Category.objects.filter(title=title).exists():
                        title = Category.objects.create(title=title,description=description)
                        response['status'] = True
                        response['message'] = 'Added successfully'
                    else:
                        response['status'] = False
                        response['message'] = 'Category Already exists'
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Edit Category'
            response['valid_form'] = False
            response['template'] = render_to_string('web/category/category_form.html', context, request=request)
        return JsonResponse(response)
    

class CategoryUpdate(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        data = {}
        obj = get_object_or_404(Category, id = id)
        form = CategoryForm(instance=obj)
        context = {'form': form, 'id': id}
        data['status'] = True
        data['title'] = 'Edit Category'
        data['template'] = render_to_string('web/category/category_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data, response = {} , {}
        id = kwargs.get('pk', None)
        obj = get_object_or_404(Category, id=id)
        previous_name = obj.title
        form = CategoryForm(request.POST or None, instance=obj)

        if form.is_valid():
            try:
                with transaction.atomic():
                    if Category.objects.filter(title__icontains=request.POST.get('title')).exclude(id=id).exists():
                        response['status'] = False
                        response['message'] = "title already exists"
                        return JsonResponse(response)
                    obj.title = request.POST.get('title' or None)
                    obj.description = request.POST.get('description' or None)
                    obj.save()

                    response['status'] = True
                    response['message'] = "Category updated successfully"
                    return JsonResponse(response)
                
            except Exception as dberror:
                response['message'] = "Something went wrong"
                response['status'] = True
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Edit Category'
            response['valid_form'] = False
            response['template'] = render_to_string('web/category/category_form.html', context, request=request)
            return JsonResponse(response)
        
class CategoryDetail(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        data = {}
        obj = get_object_or_404(Category, id = id)
        context = {'form': obj, 'id': id}
        data['status'] = True
        data['title'] = 'View Category'
        data['template'] = render_to_string('web/category/category_view.html', context, request=request)
        return JsonResponse(data)
    
class CategoryDelete(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        response = {}
        obj = get_object_or_404(Category, id = id)
        obj.delete()
        
        response['status'] = True
        response['message'] = "Category deleted successfully"
        return JsonResponse(response)
    
def change_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print('data===',data)
        category_id = data['id']
        is_active = data['is_active']
        category = get_object_or_404(Category, id=category_id)
        category.is_active = is_active
        category.save()
        response = {'status': 'success', 'is_active': category.is_active}
        return JsonResponse(response, status=200)
    else:
        response = {'status': 'error', 'message': 'Invalid request'}
        return JsonResponse(response, status=400)