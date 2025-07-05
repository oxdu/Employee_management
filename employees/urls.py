from django.urls import path
from . import views
from .import api_views
urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('form-builder/', views.form_builder, name='form_builder'),
    path('employee-form/', views.employee_form, name='employee_form'),
    path('employee-form/<int:form_id>/', views.employee_form, name='employee_form_with_id'),

    path('forms/', api_views.api_forms, name='api_forms'),
    path('employees/', api_views.api_employees, name='api_employees'),
    path('employees/<int:pk>/', api_views.api_employee_detail, name='api_employee_detail'),

]