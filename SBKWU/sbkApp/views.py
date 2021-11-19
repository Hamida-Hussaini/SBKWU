from datetime import datetime
from datetime import date
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.db import connection
# Create your views here.
from collections import namedtuple
def home(request):
    return render(request,'home.html')

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# ======================Mark Attendance
def markAttendance(request):
    context ={}
    context["currentDate"] = date.today()
    try:

        if request.method == "POST":
            date_time_str = request.POST.get("atdDate")
            date_time_obj = datetime.strptime(date_time_str, '%d-%m-%Y')
            # date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
            # print(date_time_obj.date())
            with connection.cursor() as cursor:
                cursor.callproc('InsertAttendanceRecord', [date_time_obj.date()])
            with connection.cursor() as cursor1:
                cursor1.callproc('getAttendanceRecord', [date_time_obj.date()])
                context["dataset"] = dictfetchall(cursor1)
                print(context["dataset"])
        else:
            with connection.cursor() as cursor:
                cursor.callproc('ExtractAttendanceData', [datetime.date.now()])
                context["dataset"] = dictfetchall(cursor)

    except connection.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        # if (connection.is_connected()):
        #     cursor.close()
        #     connection.close()
        #     print("MySQL connection is closed")
        with connection.cursor() as cursor2:
            cursor2.execute("SELECT DISTINCT(DATE_FORMAT(atdDate, '%Y-%m-%d')) as atDate from sbk_attendance")
            context["disableDates"] = dictfetchall(cursor2)
        return render(request,'markAttandance.html',context)

def dailyAttendance(request):
    context ={}
    context["currentDate"] = date.today()
    try:

        if request.method == "POST":
            date_time_str = request.POST.get("atdDate")
            date_time_obj = datetime.strptime(date_time_str, '%d-%m-%Y')
            # date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
            # print(date_time_obj.date())
            with connection.cursor() as cursor1:
                cursor1.callproc('getAttendanceRecord', [date_time_obj.date()])
                context["dataset"] = dictfetchall(cursor1)
                print(context["dataset"])
        else:
            with connection.cursor() as cursor:
                cursor.callproc('getAttendanceRecord', [datetime.date.now()])
                context["dataset"] = dictfetchall(cursor)

    except connection.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        # if (connection.is_connected()):
        #     cursor.close()
        #     connection.close()
        #     print("MySQL connection is closed")
        # with connection.cursor() as cursor2:
        #     cursor2.execute("SELECT DISTINCT(DATE_FORMAT(atdDate, '%Y-%m-%d')) as atDate from sbk_attendance")
        #     context["disableDates"] = dictfetchall(cursor2)
        return render(request,'reportDailyAttendance.html',context)

def monthlyAttendance(request):
    context={}
    if request.method == "POST":
        month = request.POST.get("txtMonth")
        year = request.POST.get("txtYear")
        with connection.cursor() as cursor:
            cursor.callproc('MonthlyAttendanceReport', [month,year])
            context["dataset"] = dictfetchall(cursor)

    return render(request, 'reportMonthlyAttendance.html', context)
# ============Employee Attendance Manually
def searchEmpMark(request):
    context = {}
    if request.method == "POST":
        search = request.POST.get("txtSearch")
        context["employee"] = Employee.objects.raw("select emp.*,dep.depName from sbk_employee emp,sbk_department dep where dep.id=emp.depId And emp.Id=%s",[search])
    else:
        context["employee"] = Employee.objects.raw("select emp.*,dep.depName from sbk_employee emp,sbk_department dep where dep.id=emp.depId order by emp.id Desc Limit 10")
    return render(request, 'searchEmpMark.html', context)
def markEmpAttendance(request,empId):
    context = {}
    context["employee"] = Employee.objects.get(id=empId)
    context["currentDate"] = date.today()
    if request.method == "POST":
        form = attendanceForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                form.save()
                return redirect("/searchEmpAttendance")
            except:
                pass
    else:
        form = attendanceForm()
        context['form'] = form
    return render(request, 'markEmpAttendance.html', context)

def editEmpAttendance(request, id):
    context = {}
    EmpAtd = Attendance.objects.get(id=id)
    context["atd"] = EmpAtd
    context["employee"] = Employee.objects.get(id=EmpAtd.empId)
    return render(request,'updateEmpAttendance.html', context)

def updateEmpAttendance(request, id):
    context = {}
    EmpAtd = Attendance.objects.get(id=id)
    context["atd"] = EmpAtd
    context["employee"] = Employee.objects.get(id=EmpAtd.empId)
    form = attendanceForm(request.POST, instance=EmpAtd)
    if form.is_valid():
         form.save()
         return redirect("/searchEmpAttendance")
    return render(request, 'updateEmpAttendance.html', context)

def searchEmpAttendance(request):
    context = {}

    if request.method == "POST":
        search = request.POST.get("txtId")
        context['EmpAtd'] = Attendance.objects.raw("select atd.*,emp.Name from sbk_attendance as atd,sbk_employee as emp where emp.id=atd.empId And atd.id=%s",[search])
    else:
        context['EmpAtd'] = Attendance.objects.raw("select atd.*,emp.Name from sbk_attendance as atd,sbk_employee as emp where emp.id=atd.empId order by atd.id Desc Limit 10")

    return render(request, 'searchAttendance.html', context)
#===========Employee
def insertEmployee(request):
    context = {}
    if request.method == "POST":
        form = employeeForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                form.save()
                return redirect("/showEmployee")
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

def editEmployee(request, id):
    context = {}
    context["employee"]  = Employee.objects.get(id=id)
    context["department"] = Department.objects.all()
    return render(request,'updateEmployee.html', context)

def updateEmployee(request, id):
    context = {}
    employee = Employee.objects.get(id=id)
    form = employeeForm(request.POST, instance=employee)
    context["employee"] = employee
    context["department"] = Department.objects.all()
    if form.is_valid():
         form.save()
         return redirect("/showEmployee")
    return render(request, 'updateEmployee.html', context)

def searchEmployee(request):
    context = {}
    context["urlPath"] = "searchEmployee"
    context["title"] = "Employee Name:"

    if request.method == "POST":
        search = request.POST.get("txtSearch")+"%"
        context["employee"] = Employee.objects.raw("select emp.*,dep.depName from sbk_employee emp,sbk_department dep where dep.id=emp.depId And emp.Name LIKE %s",[search])
    else:
        context["employee"] = Employee.objects.raw("select emp.*,dep.depName from sbk_employee emp,sbk_department dep where dep.id=emp.depId")
    return render(request, 'searchEmployee.html', context)

def searchEmployeeById(request):
    context = {}
    context["urlPath"] = "searchEmployeeById"
    context["title"] = "Employee Id:"
    if request.method == "POST":
        search = request.POST.get("txtSearch")
        context["employee"] = Employee.objects.raw("select emp.*,dep.depName from sbk_employee emp,sbk_department dep where dep.id=emp.depId And emp.Id=%s",[search])
    else:
        context["employee"] = Employee.objects.raw("select emp.*,dep.depName from sbk_employee emp,sbk_department dep where dep.id=emp.depId")
    return render(request, 'searchEmployee.html', context)

def searchEmployeeByDepartment(request):
    context = {}
    context["urlPath"] = "searchEmployeeByDepartment"
    context["title"] = "Department Name:"

    if request.method == "POST":
        search = request.POST.get("txtSearch")+"%"
        context["employee"] = Employee.objects.raw("select emp.*,dep.depName from sbk_employee emp,sbk_department dep where dep.id=emp.depId And dep.depName LIKE %s",[search])
    else:
        context["employee"] = Employee.objects.raw("select emp.*,dep.depName from sbk_employee emp,sbk_department dep where dep.id=emp.depId")
    return render(request, 'searchEmployee.html', context)
# ============Department
def showDepartment(request):
    context = {}
    context["Department"] = Department.objects.all()
    return render(request, 'showAllDepartment.html', context)

def insertDepartment(request):
    context = {}
    if request.method == "POST":
        form = departmentForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                form.save()
                return redirect("/showDepartment")
            except:
                pass
    else:
        form = departmentForm()
        context['form'] = form
    return render(request, 'insertDepartment.html', context)

def editDepartment(request, id):
    context = {}
    context["department"] = Department.objects.get(id=id)
    return render(request,'updateDepartment.html', context)

def updateDepartment(request, id):
    context = {}
    department = Department.objects.get(id=id)
    form = departmentForm(request.POST, instance=department)
    if form.is_valid():
         form.save()
         return redirect("/showDepartment")
    return render(request, 'updateDepartment.html', context)

def searchDepartment(request):
    context = {}
    if request.method == "POST":
        dName = request.POST.get("txtName")+"%"
        context['department'] = Department.objects.raw("select * from sbk_department where depName LIKE %s",[dName])
    else:
        context['department'] = Department.objects.all()
    return render(request, 'searchDepartment.html', context)
# ==========Leave Type
def showLeaveType(request):
    context = {}
    context["Leave"] = Leave.objects.all()
    return render(request, 'showAllLeave.html', context)

def addLeaveType(request):
    context = {}
    if request.method == "POST":
        form = leaveForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                form.save()
                return redirect("/searchLeaveType")
            except:
                pass
    else:
        form = leaveForm()
        context['form'] = form
    return render(request, 'insertLeave.html', context)

def editLeaveType(request, id):
    context = {}
    context["Leave"] = Leave.objects.get(id=id)
    return render(request,'updateLeave.html', context)

def updateLeaveType(request, id):
    context = {}
    LeaveT = Leave.objects.get(id=id)
    form = leaveForm(request.POST, instance=LeaveT)
    if form.is_valid():
         form.save()
         return redirect("/showLeaveType")
    return render(request, 'updateLeave.html', context)

def searchLeaveType(request):
    context = {}
    if request.method == "POST":
        shName= request.POST.get("txtSearch")
        context['Leave'] = Leave.objects.raw("select * from sbk_leave where shortName = %s",[shName])
    else:
        context['Leave'] = Leave.objects.raw("select * from sbk_leave order by id Desc Limit 5")
    return render(request, 'searchLeave.html', context)
# ===============Employee Leave
def showEmpLeave(request):
    context = {}
    context["EmpLeave"] = employeeLeave.objects.all()
    return render(request, 'showEmployeeAllLeave.html', context)

def addEmpLeave(request):
    context = {}
    if request.method == "POST":
        form = employeeLeaveForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                form.save()
                return redirect("/showEmpLeave")
            except:
                pass
    else:
        form = employeeLeaveForm()
        context['form'] = form
    return render(request, 'insertEmployeeLeave.html', context)

def editEmpLeave(request, id):
    context = {}
    context["EmpLeave"] = employeeLeaveForm.objects.get(id=id)
    return render(request,'updateEmployeeLeave.html', context)

def updateEmpLeave(request, id):
    context = {}
    EmpLeave = employeeLeaveForm.objects.get(id=id)
    form = leaveForm(request.POST, instance=EmpLeave)
    if form.is_valid():
         form.save()
         return redirect("/showEmpLeave")
    return render(request, 'updateEmployeeLeave.html', context)

def searchEmpLeave(request):
    context = {}
    if request.method == "POST":
        id = request.POST.get("txtId")
        context['EmpLeave'] = employeeLeave.objects.get(id=id)
    else:
        context['EmpLeave'] = employeeLeave.objects.all()
    return render(request, 'searchEmpLeave.html', context)

