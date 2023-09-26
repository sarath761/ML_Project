
from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.login_user,name='login'),
    # path('signup',views.signup,name='signup'),
    path('csvfile/',views.csvfile,name='csvfile'),
    path('csvfileEmp/',views.csvfileEmp,name='csvfileEmp'),
    path('csvfilePrjct/',views.csvfilePrjct,name='csvfilePrjct'),
    path('home1/',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout1',views.logout_user,name='logout1'),
    path('users_csv/',views.users_csv, name='upload_csv'),
    path('project_csv/',views.project_csv, name='project_csv'),
    path('employee_list/',views.employee_list, name='employee_list'),
    path('project_list/',views.project_list, name='project_list'),
    # path('display_csv',views.display_csv),
    path('dash/',views.dash, name='dash'),
    path('CreateUser/',views.CreateUser, name='CreateUser'),
    path('register', views.register, name='register'),
    path('upload/', views.upload_file, name='upload_file'),
    path('result/', views.result, name='result'),
    
]