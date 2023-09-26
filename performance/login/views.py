from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User

from .MLtraining import train_fun

def users_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # Check if the uploaded file is a CSV
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Error: Please upload a CSV file.")
            return redirect('csvfileEmp')  # Redirect back to the upload page
        
        try:
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
            
            # Skip the header row if present
            # next(csv_data, None)
            
            added_count = 0
            duplicate_count = 0
            
            for row in csv_data:
                if row:  # Assuming each row has at least one column
                    employee_name = row[0]
                    if employee_name:
                        # Check if an employee with the same name already exists
                        if Employee_detail.objects.filter(employee_name=employee_name).exists():
                            duplicate_count += 1
                        else:
                            Employee_detail.objects.create(employee_name=employee_name)
                            added_count += 1
            
            if added_count > 0:
                messages.success(request, f"{added_count} New details stored")
            if duplicate_count > 0:
                messages.warning(request, f"{duplicate_count} employees already exist")
            if added_count == 0 and duplicate_count == 0:
                messages.error(request, "No valid data found in the file")
        
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        
        return redirect('csvfileEmp')  # Redirect back to the upload page

def project_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file2'):
        csv_file = request.FILES['csv_file2']

        # Check if the uploaded file is a CSV
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Error: Please upload a CSV file.")
            return redirect('csvfilePrjct')  # Redirect back to the upload page
        
        try:
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
            
            # Skip the header row if present
            # next(csv_data, None)
            
            added_count = 0
            duplicate_count = 0
            
            for row in csv_data:
                if row:  # Assuming each row has at least one column
                    project_name = row[0]
                    if project_name:
                        # Check if an employee with the same name already exists
                        if Project.objects.filter(project_name=project_name).exists():
                            duplicate_count += 1
                        else:
                            Project.objects.create(project_name=project_name)
                            added_count += 1
            
            if added_count > 0:
                messages.success(request, f"{added_count} New details stored")
            if duplicate_count > 0:
                messages.warning(request, f"{duplicate_count} Projects already exist")
            if added_count == 0 and duplicate_count == 0:
                messages.error(request, "No valid data found in the file")
        
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        
        return redirect('csvfilePrjct')  # Redirect back to the upload page


def project_list(request):
    projects = Project.objects.order_by('project_name')
    return render(request, 'project_list.html', {'projects': projects})

def employee_list(request):
    employees = Employee_detail.objects.order_by('employee_name')
    return render(request, 'employee_list.html', {'employees': employees})






def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out!"))
    return redirect('/')



# @login_required
def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if the input is an email
        if '@' in username:
            user = User.objects.filter(email=username).first()
            if user is not None:
                username = user.username

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # user_role = "admin" if user.is_staff else "user"
                return redirect('dash')
            else:
                messages.error(request, "Your account is not active.")
        else:
            messages.error(request, "Invalid credentials. Please enter the correct username/email and password.")
    return render(request, 'login.html')






def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['first_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        gender = request.POST.get('gender')  # Retrieve selected gender
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        
        try:
            user_profile = UserProfile.objects.get(first_name=first_name)
            has_user_profile = True
        except UserProfile.DoesNotExist:
            user_profile = None
            has_user_profile = False
        
        messages.success(request, f'New user created: {username}')
        return redirect('CreateUser')  # Redirect to the same page
    return render(request, 'create-user.html')


def home(request):
    return render(request,'home.html')


def dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        # user_role = "admin" if request.user.is_staff else "user"
    except UserProfile.DoesNotExist:
        user_profile = None
        # user_role = "user"
    
    context = {
        'active_user_profile': user_profile,
        # 'user_role': user_role,  # Pass the user role to the template
    }

    return render(request, 'dashboard.html', context)


def csvfile(request):
    return render(request,'csvfile.html')

def csvfileEmp(request):
    return render(request,'csvfileEmp.html')

def csvfilePrjct(request):
    return render(request,'csvfilePrjct.html')

def get_emp_last_update_date():
    try:
        latest_employee = Employee_detail.objects.order_by('-last_inserted').first()
        return latest_employee.last_inserted
    except Employee_detail.DoesNotExist:
        return None  # Handle the case when there are no employees in the database


def get_last_project_insert_date():
    try:
        latest_project = Project.objects.order_by('-last_prct_inserted').first()
        return latest_project.last_prct_inserted
    except Project.DoesNotExist:
        return None  # Handle the case when there are no projects in the database


def dash(request):
    employee_count = Employee_detail.objects.count()
    # employee_count = Employee_detail.objects.get()
    project_count = Project.objects.count()
    last_update_date = get_emp_last_update_date()
    last_project_insert_date = get_last_project_insert_date()
    employees = Employee_detail.objects.order_by('employee_name')
    projects = Project.objects.order_by('project_name')
    context = {
        'employee_count': employee_count, 
        'project_count': project_count,
        'last_update_date': last_update_date,
        'last_project_insert_date': last_project_insert_date,
        'employees': employees,
        'projects': projects
    }
    return render(request, 'dash-content.html', context)




def CreateUser(request):

    return render(request,'create-user.html')



def upload_file(request):
    if request.method == 'POST':
        report = request.FILES['report']
        activity = request.FILES['activity']

        EmployeeModel.objects.create(report=report, activity=activity)

        messages.success( request, "Document uploaded successfully 😎.")
    return redirect(request.META.get('HTTP_REFERER'))



def result(request):
    # if request.method == 'POST':
        # id = request.POST.get(id)

        emp_obj = EmployeeModel.objects.last()
        path1 = emp_obj.report.path
        path2 = emp_obj.activity.path
        
        image = train_fun(path1, path2)
        return render(request, 'result.html', {'image':image})
    
    # return render(request, 'csvfile.html')