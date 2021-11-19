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

class leaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'

class employeeLeaveForm(forms.ModelForm):
    class Meta:
        model = employeeLeave
        fields = '__all__'

class attendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'