from django import forms
from .models import *

class departmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class employeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'