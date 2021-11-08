from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('addEmployee', views.insertEmployee, name='insertEmp'),
    path('showEmployee', views.showEmployee, name='showAllEmployee'),
    path('addDepartment', views.insertDepartment, name='insertDep'),
]