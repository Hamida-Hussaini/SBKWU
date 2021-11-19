from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('addEmployee', views.insertEmployee, name='insertEmp'),
    path('showEmployee', views.showEmployee, name='showAllEmployee'),
    path('editEmployee/<int:id>', views.editEmployee,name='editEmployee'),
    path('updateEmployee/<int:id>', views.updateEmployee,name='updateEmployee'),
    path('searchEmployee', views.searchEmployee, name='searchEmployee'),
    path('searchEmployeeById', views.searchEmployeeById, name='searchEmployee'),
    path('searchEmployeeByDepartment', views.searchEmployeeByDepartment, name='searchEmployee'),

    path('showDepartment', views.showDepartment, name='showAllEmployee'),
    path('addDepartment', views.insertDepartment, name='insertDep'),
    path('editDepartment/<int:id>', views.editDepartment, name='editDepartment'),
    path('updateDepartment/<int:id>', views.updateDepartment, name='updateDepartment'),
    path('searchDepartment', views.searchDepartment, name='searchDepartment'),

    path('markAttendance', views.markAttendance, name='markAttendance'),
    path('monthlyAttendance', views.monthlyAttendance, name='monthlyAttendance'),
    path('dailyAttendance', views.dailyAttendance, name='monthlyAttendance'),

    path('markEmpAttendance/<int:empId>', views.markEmpAttendance, name='markEmpAttendance'),
    path('editEmpAttendance/<int:id>', views.editEmpAttendance, name='editEmpAttendance'),
    path('updateEmpAttendance/<int:id>', views.updateEmpAttendance, name='updateEmpAttendance'),
    path('searchEmpAttendance', views.searchEmpAttendance, name='searchEmpAttendance'),
    path('searchEmpMark', views.searchEmpMark, name='searchEmpMark'),

    path('showLeaveType', views.showLeaveType, name='showLeaveType'),
    path('addLeaveType', views.addLeaveType, name='addLeaveType'),
    path('editLeaveType/<int:id>', views.editLeaveType, name='editLeaveType'),
    path('updateLeaveType/<int:id>', views.updateLeaveType, name='updateLeaveType'),
    path('searchLeaveType', views.searchLeaveType, name='searchLeaveType'),

    path('showEmpLeave', views.showEmpLeave, name='showEmpLeave'),
    path('addEmpLeave', views.addEmpLeave, name='addEmpLeave'),
    path('editEmpLeave/<int:id>', views.editEmpLeave, name='editEmpLeave'),
    path('updateEmpLeave/<int:id>', views.updateEmpLeave, name='updateEmpLeave'),
    path('searchEmpLeave', views.searchEmpLeave, name='searchEmpLeave'),



]