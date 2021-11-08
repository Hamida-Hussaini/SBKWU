from django.shortcuts import render,redirect
from .models import *
from .forms import *
# Create your views here.
def home(request):
    return render(request,'home.html')

def insertEmployee(request):
    context = {}
    if request.method == "POST":
        form = employeeForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                form.save()
                return redirect('showEmployee')
            except:
                pass
        context['form'] = form
    else:
        form = employeeForm()
        context['form'] = form
    context["department"] = Department.objects.all()
    return render(request, 'insertEmployee.html', context)

def showEmployee(request):
    context = {}
    context["employee"] = Employee.objects.raw("select emp.*,dep.depName from sbk_employee emp,sbk_department dep where dep.id=emp.depId")
    return render(request, 'showAllEmployee.html', context)

def insertDepartment(request):
    context = {}
    if request.method == "POST":
        form = departmentForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                form.save()
                return redirect('addDepartment')
            except:
                pass
    else:
        form = departmentForm()
        context['form'] = form
    return render(request, 'insertDepartment.html', context)
