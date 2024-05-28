from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from swift.forms.tool_template import * 
from swift.helper import renderfile, is_ajax, LogUserActivity
from swift.models import ToolInput,ToolType,ToolTemplateInput,ToolTemplate,ToolKeyword
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from swift.models import CREATE,  UPDATE, SUCCESS, FAILED, DELETE, READ
from django.db import transaction
import pdb



class ToolTemplateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': ToolTemplateForm(),
            'inp_form': ToolInputForm()
        }
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            response = {
                'status': True,
                'template': render_to_string('swift/tooltemplate/tool_template_form.html', context, request=request)
            }
            return JsonResponse(response)
        
        return render(request, 'swift/tooltemplate/index.html', context)

    def post(self, request, *args, **kwargs):
        form = ToolTemplateForm(request.POST, request.FILES)
        inp_form = ToolInputForm(request.POST)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid() and inp_form.is_valid():
                tool_template_instance = form.save(commit=False)
                tool_input_instance = inp_form.save(commit=False)
                tool_type_id = form.cleaned_data['tool_type']
                tool_input_id = inp_form.cleaned_data['tool_template']
                tool_type = get_object_or_404(ToolType, pk=tool_type_id)
                tool_input = get_object_or_404(ToolInput, pk=tool_input_id)
                tool_template_instance.tool_type = tool_type
                tool_input_instance.tool_template = tool_input
                tool_template_instance.save()
                tool_input_instance.save()
                form.save()
                inp_form.save()
            
                inputs_data = {
                    'place_holder': request.POST.getlist('place_holder'),
                    'description': request.POST.getlist('description')
                }

                ToolTemplateInput.objects.create(
                    tool_template=tool_template_instance,
                    tool_input=tool_input_instance,
                    inputs=inputs_data,
                    validation_message=inp_form.cleaned_data['validation_message'],
                    sort_order=inp_form.cleaned_data['sort_order']
                )

                response = {
                    'status': True,
                    'message': 'Form submitted successfully!'
                }
            else:
                response = {
                    'status': False,
                    'form_errors': form.errors,
                    'inp_form_errors': inp_form.errors
                }
            return JsonResponse(response)
        else:
            if form.is_valid() and inp_form.is_valid():
                tool_template_instance = form.save(commit=False)
                tool_input_instance = inp_form.save(commit=False)
                tool_type_id = form.cleaned_data['tool_type']
                tool_input_id = inp_form.cleaned_data['tool_template']
                tool_type = get_object_or_404(ToolType, pk=tool_type_id)
                tool_input = get_object_or_404(ToolInput, pk=tool_input_id)
                tool_template_instance.tool_type = tool_type
                tool_input_instance.tool_template = tool_input
                tool_template_instance.save()
                tool_input_instance.save()
                form.save()
                inp_form.save()

               
                inputs_data = {
                    'place_holder': request.POST.getlist('place_holder'),
                    'description': request.POST.getlist('description')
                }
                
                
                ToolTemplateInput.objects.create(
                    tool_template=tool_template_instance,
                    tool_input=tool_input_instance,
                    inputs=inputs_data,
                    validation_message=inp_form.cleaned_data['validation_message'],
                    sort_order=inp_form.cleaned_data['sort_order']
                )
                return redirect('appswift:tooltemplate_create')
            else:
                context = {
                    'form': form,
                    'inp_form': inp_form
                }
                return render(request, 'swift/tooltemplate/index.html', context)
    
