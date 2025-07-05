from rest_framework import serializers
from .models import DynamicForm, FormField, Employee, EmployeeData

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'label', 'field_type', 'required', 'order']

class DynamicFormSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True, read_only=True)
    
    class Meta:
        model = DynamicForm
        fields = ['id', 'name', 'created_at', 'fields']

class EmployeeDataSerializer(serializers.ModelSerializer):
    field_label = serializers.CharField(source='field.label', read_only=True)
    
    class Meta:
        model = EmployeeData
        fields = ['field', 'field_label', 'value']

class EmployeeSerializer(serializers.ModelSerializer):
    data = EmployeeDataSerializer(many=True, read_only=True)
    form_name = serializers.CharField(source='form.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'form', 'form_name', 'created_at', 'updated_at', 'data']