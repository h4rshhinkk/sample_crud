# class RegionView(PermissionRequiredMixin,View):
#     permission_required = 'higo.view_region'
#     def get(self, request, args, *kwargs):
#         form = RegionForm()
#         data = {}
#         context_data = get_country(request)
#         own_country = context_data.get('own_country')
#         country = request.GET.get('country',own_country.id)
#         data['form'] = form
#         # data['countries'] = Countries.objects.filter(is_active=True).order_by('-id')
#         data['datas'] = Region.objects.select_related('country').filter(is_active=True,country_id = country).order_by('-id')
#         return renderfile(request,'region','index',data)

# class CreateRegion(PermissionRequiredMixin,View):
#     permission_required = 'higo.add_region'
#     def get(self, request, args, *kwargs):
#         form = RegionForm()
#         data = {}
#         context = {'form': form}
#         data['status'] = True
#         data['title'] = "Add Region"
#         template = get_template('administrator/region/region_ajax_form.html')
#         data['html_temp'] = template.render(context,request)
#         return JsonResponse(data)
#     def post(self,request,*args, **kwargs):
#         data = {}
#         form = RegionForm(request.POST or None)
#         if form.is_valid(): 
#             try:
#                 with transaction.atomic():   
#                     name = form.cleaned_data.get('name')
#                     country = form.cleaned_data.get('country')
#                     obj = Region()
#                     obj.name = name
#                     obj.country = country
#                     obj.save()
#                     data['form_is_valid'] = True
#                     data['status'] = True
#                     data['message'] = 'Region Added Successfully'
#                     log_data = {}
#                     log_data['module_name'] = 'CreateRegion'
#                     log_data['action_type'] = CREATE
#                     log_data['log_message'] = f'Region {obj.name} Added Successfully'
#                     log_data['status'] = SUCCESS
#                     log_data['model_object'] = obj
#                     log_data['db_data'] = {'id':obj.id}
#                     log_data['app_visibility'] = False
#                     log_data['web_visibility'] = True
#                     log_data['error_msg'] = ''
#                     log_data['fwd_link'] = f"/region/create/"
#                     LogUserActivity(request, log_data)
#                     return JsonResponse(data)
#             except Exception as e:     
#                 data['form_is_valid'] = False
#                 data['status'] = False
#                 log_data = {}
#                 log_data['module_name'] = 'CreateRegion'
#                 log_data['action_type'] = CREATE
#                 log_data['log_message'] = 'Region creation failed'
#                 log_data['status'] = FAILED
#                 log_data['model_object'] = None
#                 log_data['db_data'] = {}
#                 log_data['app_visibility'] = False
#                 log_data['web_visibility'] = False
#                 log_data['error_msg'] = str(e)
#                 log_data['fwd_link'] = f"/region/create/"
#                 LogUserActivity(request, log_data)
#                 return JsonResponse(data)
#         else:
#             data['form_is_valid'] = False
#             data['status'] = False
#             data['title'] = "Add Region"
#             context = {'form': form}
#             template = get_template('administrator/region/region_ajax_form.html')
#             data['html_temp'] = template.render(context,request)
#             log_data = {}
#             log_data['module_name'] = 'CreateRegion'
#             log_data['action_type'] = CREATE
#             log_data['log_message'] = 'Region creation failed'
#             log_data['status'] = FAILED
#             log_data['model_object'] = None
#             log_data['db_data'] = {}
#             log_data['app_visibility'] = False
#             log_data['web_visibility'] = False
#             log_data['error_msg'] = str(form.errors)
#             log_data['fwd_link'] = f"/region/create/"
#             LogUserActivity(request, log_data)
#             return JsonResponse(data)

# class UpdateRegion(PermissionRequiredMixin,View):
#     permission_required = 'higo.change_region'
#     def get(self, request, args, *kwargs):
#         id = kwargs.get('pk', None)
#         obj = get_object_or_404(Region,id = id)	
#         form = RegionForm(instance=obj)
#         data = {}
#         context = {'form': form}
#         data['status'] = True
#         data['title'] = "Edit Region"
#         template = get_template('administrator/region/region_ajax_form.html')
#         data['html_temp'] = template.render(context,request)
#         return JsonResponse(data)
#     def post(self,request,*args, **kwargs):
#         data = {}
#         id = kwargs.get('pk', None)
#         obj = get_object_or_404(Region,id = id)	
#         form = RegionForm(request.POST or None,instance=obj)
#         if form.is_valid(): 
#             try:
#                 with transaction.atomic():   
#                     name = form.cleaned_data.get('name')
#                     country = form.cleaned_data.get('country')
#                     obj.name = name
#                     obj.country = country
#                     obj.save()
#                     data['form_is_valid'] = True
#                     data['status'] = True
#                     data['message'] = 'Region Updated Successfully'
#                     log_data = {}
#                     log_data['module_name'] = 'UpdateRegion'
#                     log_data['action_type'] = UPDATE
#                     log_data['log_message'] = f'Region {obj.name} Updated Successfully'
#                     log_data['status'] = SUCCESS
#                     log_data['model_object'] = obj
#                     log_data['db_data'] = {'id':obj.id}
#                     log_data['app_visibility'] = False
#                     log_data['web_visibility'] = True
#                     log_data['error_msg'] = ''
#                     log_data['fwd_link'] = f"/region/{id}/update/"
#                     LogUserActivity(request, log_data)
#                     return JsonResponse(data)
#             except Exception as e:   
#                 data['form_is_valid'] = False
#                 data['status'] = False
#                 log_data = {}
#                 log_data['module_name'] = 'UpdateRegion'
#                 log_data['action_type'] = UPDATE
#                 log_data['log_message'] = f'Region {obj.name} updation failed'
#                 log_data['status'] = FAILED
#                 log_data['model_object'] = obj
#                 log_data['db_data'] = {'id':obj.id}
#                 log_data['app_visibility'] = False
#                 log_data['web_visibility'] = False
#                 log_data['error_msg'] = str(e)
#                 log_data['fwd_link'] = f"/region/{id}/update/"
#                 LogUserActivity(request, log_data)
#                 return JsonResponse(data)
#         else:        
#             data['form_is_valid'] = False
#             data['status'] = False
#             data['title'] = "Edit Region"
#             context = {'form': form}
#             template = get_template('administrator/region/region_ajax_form.html')
#             data['html_temp'] = template.render(context,request)
#             log_data = {}
#             log_data['module_name'] = 'UpdateRegion'
#             log_data['action_type'] = UPDATE
#             log_data['log_message'] = f'Region {obj.name} updation failed'
#             log_data['status'] = FAILED
#             log_data['model_object'] = obj
#             log_data['db_data'] = {'id':obj.id}
#             log_data['app_visibility'] = False
#             log_data['web_visibility'] = False
#             log_data['error_msg'] = str(form.errors)
#             log_data['fwd_link'] = f"/region/{id}/update/"
#             LogUserActivity(request, log_data)
#             return JsonResponse(data)

# class DeleteRegion(PermissionRequiredMixin,View):
#     permission_required = 'higo.delete_region'
#     def get(self,request,*args, **kwargs):
#         try:
#             data = {}
#             id = kwargs.get('pk', None)	
#             region_obj = Region.objects.filter(id=id).last()
#             store_obj = Store.objects.select_related('region').filter(region = region_obj)
#             store_count = store_obj.count()
#             if store_count>0:
#                 data['store_exist'] = 'true'
#                 if store_count == 1:
#                     data['store_exist_message'] = f"{store_count} Store exist in this region"
#                 else:
#                     data['store_exist_message'] = f"{store_count} Stores exists in this region"
#             data['status']=True
#         except Exception as e:
#             data['status']=False
#             data['message']=str(e)
#         return JsonResponse(data)
#     def post(self,request,*args, **kwargs):
#         id = kwargs.get('pk', None)	
#         data = {}
#         try:
#             obj = get_object_or_404(Region, id = id) 
#             obj.is_active = False
#             obj.save()
#             data['status']  = True
#             data['message']  = "Region Deleted Successfully"
#             log_data = {}
#             log_data['module_name'] = 'DeleteRegion'
#             log_data['action_type'] = DELETE
#             log_data['log_message'] = f"Region {obj.name} Deleted Successfully"
#             log_data['status'] = SUCCESS
#             log_data['model_object'] = obj
#             log_data['db_data'] = {'id':obj.id}
#             log_data['app_visibility'] = False
#             log_data['web_visibility'] = True
#             log_data['error_msg'] = ''
#             log_data['fwd_link'] = f"/region/{id}/delete/"
#             LogUserActivity(request, log_data)
#         except Exception as e:
#             data['status']=False
#             data['message']=str(e)
#             log_data = {}
#             log_data['module_name'] = 'DeleteRegion'
#             log_data['action_type'] = DELETE
#             log_data['log_message'] = f"Region deletion failed"
#             log_data['status'] = FAILED
#             log_data['model_object'] = None
#             log_data['db_data'] = {}
#             log_data['app_visibility'] = False
#             log_data['web_visibility'] = False
#             log_data['error_msg'] = str(e)
#             log_data['fwd_link'] = f"/region/{id}/delete/"
#             LogUserActivity(request, log_data)
#         return JsonResponse(data)
        

# class RegionFilter(PermissionRequiredMixin,View):
#     permission_required = 'higo.view_region'
#     def get(self, request, args, *kwargs):
#         search_term = request.GET.get('search_term', None)
#         # country = request.GET.get('country', None)
#         context_data = get_country(request)
#         own_country = context_data.get('own_country')
#         country = request.GET.get('country',own_country.id)
#         conditions = {}
#         conditions['is_active'] = True
#         if country:
#             conditions['country_id'] = country

#         if search_term:
#             search_term = search_term.lower()
#             q_filter = (Q(name__icontains=search_term))
#             if country:
#                 q_filter &= Q(country_id=country) 
#             # conditions['name__icontains'] = search_term
#             region_list = Region.objects.select_related('country').filter(q_filter,is_active=True).order_by('-id')
#         else:   
#             region_list = Region.objects.select_related('country').filter(**conditions).order_by('-id')

#         page = request.GET.get('current_page', 1)
#         paginator = Paginator(region_list, PAGINATION_PERPAGE)
#         try:
#             region = paginator.page(page)

#         except PageNotAnInteger:
#             region = paginator.page(1)
#         except EmptyPage:
#             region = paginator.page(paginator.num_pages)

#         new_data = []
#         for data in region:
#             new_data.append({'id': data.id, 'name': data.name,'country':data.country.name,'country_id':data.country.id})

#         template = get_template('administrator/region/region_list_table_ajax.html')
#         current_page = int(page)

#         html_temp = template.render({'datas': region, 'current_page': current_page}, request)

#         pagination_template = get_template('administrator/region/pagination.html')

#         pagination = pagination_template.render({'datas': region, 'current_page': current_page}, request)

#         if current_page:
#             pointing = current_page - 1
#         else:
#             pointing = 0
#         limit = int(PAGINATION_PERPAGE)
#         offset = limit * pointing
#         return JsonResponse({'html_temp': html_temp, 'data_list': new_data, 'limit': limit, 'offset': offset, 'pagination': pagination})