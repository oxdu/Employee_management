from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DynamicForm, FormField, Employee, EmployeeData
from .serializers import DynamicFormSerializer, EmployeeSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_forms(request):
    if request.method == 'GET':
        forms = DynamicForm.objects.filter(created_by=request.user)
        serializer = DynamicFormSerializer(forms, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        form = DynamicForm.objects.create(
            name=request.data.get('name'),
            created_by=request.user
        )
        
        for idx, field_data in enumerate(request.data.get('fields', [])):
            FormField.objects.create(
                form=form,
                label=field_data['label'],
                field_type=field_data['type'],
                required=field_data.get('required', True),
                order=idx
            )
        
        serializer = DynamicFormSerializer(form)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_employees(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        search = request.query_params.get('search')
        if search:
            employee_ids = EmployeeData.objects.filter(
                value__icontains=search
            ).values_list('employee_id', flat=True)
            employees = employees.filter(id__in=employee_ids)
        
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        form_id = request.data.get('form_id')
        form = DynamicForm.objects.get(id=form_id)
        
        employee = Employee.objects.create(form=form)
        
        for field_data in request.data.get('fields', []):
            EmployeeData.objects.create(
                employee=employee,
                field_id=field_data['field_id'],
                value=field_data['value']
            )
        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Update employee data
        for field_data in request.data.get('fields', []):
            EmployeeData.objects.update_or_create(
                employee=employee,
                field_id=field_data['field_id'],
                defaults={'value': field_data['value']}
            )
        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)