from django.db import models

# Create your models here.
class Department(models.Model):
    depName = models.CharField(max_length=70)

    class Meta:
        db_table = "sbk_department"

class Employee(models.Model):
    depId= models.IntegerField()
    Name = models.CharField(max_length=30)
    FatherName = models.CharField(max_length=30)
    genders = (('Female', 'Female'),('Male', 'Male'))
    gender = models.CharField(max_length=10, choices=genders,default='Female')
    dob = models.DateField()
    CNIC = models.CharField(max_length=20)
    contact_No = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address = models.TextField()
    pic = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = "sbk_employee"

class Attendance(models.Model):
    empId= models.IntegerField()
    atdDate = models.DateField()
    inTime = models.TimeField(blank=True)
    outTime = models.TimeField(blank=True)
    status = models.CharField(max_length=20)
    class Meta:
        db_table = "sbk_attendance"


class Leave(models.Model):
    LeaveType = models.CharField(max_length=100)
    shortName = models.CharField(max_length=20)
    class Meta:
        db_table = "sbk_leave"

class employeeLeave(models.Model):
    empId= models.IntegerField()
    leaveDate = models.DateField()
    leaveId = models.IntegerField()

    class Meta:
        db_table = "sbk_empLeave"

class deviceAttendance(models.Model):
    empId= models.IntegerField()
    TimeStamp = models.DateTimeField()
    class Meta:
        db_table = "sbk_deviceAttendance"