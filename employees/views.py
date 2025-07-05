from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DynamicForm, FormField, Employee, EmployeeData
import json

@login_required
def form_builder(request):
    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        fields_data = json.loads(request.POST.get('fields'))
        
        form = DynamicForm.objects.create(
            name=form_name,
            created_by=request.user
        )
        
        for idx, field in enumerate(fields_data):
            FormField.objects.create(
                form=form,
                label=field['label'],
                field_type=field['type'],
                required=field.get('required', True),
                order=idx
            )
        
        return JsonResponse({'success': True, 'form_id': form.id})
    
    forms = DynamicForm.objects.filter(created_by=request.user)
    return render(request, 'form_builder.html', {'forms': forms})

@login_required
def employee_form(request, form_id=None):
    forms = DynamicForm.objects.filter(created_by=request.user)
    
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        form = get_object_or_404(DynamicForm, id=form_id)
        
        employee = Employee.objects.create(form=form)
        
        for field in form.fields.all():
            value = request.POST.get(f'field_{field.id}')
            if value:
                EmployeeData.objects.create(
                    employee=employee,
                    field=field,
                    value=value
                )
        
        return JsonResponse({'success': True, 'employee_id': employee.id})
    
    selected_form = None
    if form_id:
        selected_form = get_object_or_404(DynamicForm, id=form_id)
    
    return render(request, 'employee_form.html', {
        'forms': forms,
        'selected_form': selected_form
    })

@login_required
def employee_list(request):
    employees = Employee.objects.all().prefetch_related('data', 'data__field')
    
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        employee_id = request.POST.get('employee_id')
        Employee.objects.filter(id=employee_id).delete()
        return JsonResponse({'success': True})
    
    search_query = request.GET.get('search', '')
    if search_query:
        employee_ids = EmployeeData.objects.filter(
            value__icontains=search_query
        ).values_list('employee_id', flat=True)
        employees = employees.filter(id__in=employee_ids)
    
    return render(request, 'employee_list.html', {'employees': employees})