from django.db import models

# Create your models here.
class Department(models.Model):
    depName = models.CharField(max_length=70)

    class Meta:
        db_table = "sbk_department"

class Employee(models.Model):
    departmentsList = []
    department = Department.objects.all()
    for i in department:
        departmentsList.append((i.id, i.depName))
    depId= models.IntegerField(choices=departmentsList,default=1)
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