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
import json



class ToolTemplateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': ToolTemplateForm(),
            'inp_form': ToolInputForm(),
            'item_formset': ToolInputFormFormSet()
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            tool_input_value = request.GET.get('tool_input')
            additional_fields_html = ""

            # Logic to determine additional fields based on tool_input_value
            if tool_input_value:
                try:
                    tool_input = ToolTemplateInput.objects.get(name=tool_input_value)
                    # Depending on your model structure, you can fetch related fields or data here
                    # For simplicity, let's assume tool_input has a related field called additional_fields
                    additional_fields = tool_input.tool_input.all()
                    context['additional_fields'] = additional_fields
                    additional_fields_html = render_to_string('swift/tooltemplate/additional_fields.html', context)
                except ToolInput.DoesNotExist:
                    pass  # Handle the case where the tool_input doesn't exist

            return JsonResponse({'additional_fields_html': additional_fields_html})

        return render(request, 'swift/tooltemplate/index.html', context)

    def post(self, request, *args, **kwargs):
        form = ToolTemplateForm(request.POST, request.FILES)
        inp_form = ToolInputForm(request.POST)
        item_formset = ToolInputFormFormSet(request.POST)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid() and inp_form.is_valid() and item_formset.is_valid():
                try:
                    with transaction.atomic():
                        tool_template_instance = form.save()
                        tool_input_instance = inp_form.save(commit=False)
                        tool_input_instance.tool_template = tool_template_instance
                        tool_input_instance.save()
                        item_formset.instance = tool_template_instance
                        item_formset.save()
                    
                    response = {
                        'status': True,
                        'message': 'Form submitted successfully!'
                    }
                except Exception as e:
                    response = {
                        'status': False,
                        'message': 'Error occurred while saving form data.'
                    }
            else:
                response = {
                    'status': False,
                    'form_errors': form.errors,
                    'inp_form_errors': inp_form.errors,
                    'item_formset_errors': item_formset.errors
                }
            return JsonResponse(response)

class ToolTemplateInputCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ToolInputForm()
        context = {'form': form, 'id': 0}
        data = {
            'status': True,
            'title': 'Add Inputs',
            'template': render_to_string('swift/tooltemplate/input_details_form.html', context, request=request)
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        inputs_data = {
            'place_holder': request.POST.getlist('place_holder'),
            'description': request.POST.getlist('description'),
            'max_length': request.POST.getlist('max_length'),
            'inp_validation_msg1': request.POST.getlist('inp_validation_msg1'),
            'min_length': request.POST.getlist('min_length'),
            'inp_validation_msg2': request.POST.getlist('inp_validation_msg2')
        }

        form = ToolInputForm(request.POST or None, initial={'data': inputs_data})
        if form.is_valid():
            try:
                with transaction.atomic():
                    tool_template = request.POST.get('tool_template', None)
                    if not ToolTemplateInput.objects.filter(tool_template=tool_template).exists():
                        obj = ToolTemplateInput.objects.create(tool_template=tool_template, inputs=json.dumps(inputs_data))
                        response = {'status': True, 'message': 'Added successfully'}
                    else:
                        response = {'status': False, 'message': 'Inputs Already exists'}
            except Exception as e:
                response = {'status': False, 'message': 'Error occurred while saving form data.'}
        else:
            context = {'form': form}
            response = {
                'status': False,
                'title': 'Add Inputs',
                'valid_form': False,
                'template': render_to_string('swift/tooltemplate/input_details_form.html', context, request=request)
            }
        return JsonResponse(response)