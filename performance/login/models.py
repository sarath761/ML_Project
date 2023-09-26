from django.db import models
from django.contrib.auth.models import User
import os
import uuid
# from django.contrib.auth.models import AbstractUser
# Employee model

class Employee_detail(models.Model):
    id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=100)
    last_inserted = models.DateTimeField(auto_now_add=True)  # Automatically set when a new record is created

    def __str__(self):
        return self.employee_name

# Project model

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    last_prct_inserted = models.DateTimeField(auto_now_add=True)  # Automatically set when a new record is created
    def __str__(self):
        return self.project_name
    
class WorkingTime(models.Model):
    emp_id = models.ForeignKey(Employee_detail,on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    percentage = models.CharField(max_length=10)
    time = models.CharField(max_length=20,blank=True,null=True)
    # def __str__(self):
    #     return self.emp_id
    class Meta:
        unique_together = ('emp_id', 'project_id')
    


class UserProfile(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number= models.CharField(max_length=20,blank=True,null=True)
    gender=models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return self.user_id
    



def generate_unique_filename(instance, filename):
    base_name, extension = os.path.splitext(filename)
    unique_id = uuid.uuid4().hex
    return f"{unique_id}{extension}"

class EmployeeModel(models.Model):
    activity = models.FileField(upload_to=generate_unique_filename, max_length=200)
    report = models.FileField(upload_to=generate_unique_filename, max_length=200)


# class CustomUser(AbstractUser):
#     full_name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20)
#     gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])

#     # Customize related names with your app name and class name
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name='user permissions',
#         blank=True,
#         related_name='login_%(class)s_user_permissions'
#     )
#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name='groups',
#         blank=True,
#         related_name='login_%(class)s_groups'
#     )

#     def __str__(self):
#         return self.username