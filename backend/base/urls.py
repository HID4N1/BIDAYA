#urls set up

from django.urls import path
from . import views
from .views import *



urlpatterns = [
    path('', Home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('projects/', Projects, name='projects'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('redirect/', role_redirect, name='role_redirect'),
    
    #admin area
    path('Myadmin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('Myadmin/entrepreneurs/', admin_entrepreneur, name='admin_ENT'),
    path('Myadmin/entrepreneurs/edit/<int:entrepreneur_id>/', views.edit_entrepreneur, name='edit_entrepreneur'),
    path('Myadmin/entrepreneurs/delete/<int:entrepreneur_id>/', views.delete_entrepreneur, name='delete_entrepreneur'),
    path('Myadmin/investors/', admin_investors, name='admin_INV'),
    path('Myadmin/investors/edit/<int:investisseur_id>/', views.edit_investor, name='edit_investor'),
    path('Myadmin/investors/delete/<int:investisseur_id>/', views.delete_investor, name='delete_investor'),
    path('Myadmin/notifications/', admin_notifications, name='admin_NOTIF'),
    path('Myadmin/analytics/', admin_analytics, name='admin_analytics'),
    path('Myadmin/generate_report/', admin_generate_report, name='admin_generate_report'),
    
    
    #entrepreneur area
    path('entrepreneur/dashboard/', entrepreneur_dashboard, name='entrepreneur_dashboard'),
    path('entrepreneur/projects/', entrepreneur_projects, name='entrepreneur_projects'),
    path('entrepreneur/projects/<int:project_id>/', entrepreneur_project_detail, name='entrepreneur_project_detail'),
    path('entrepreneur/projects/create/', entrepreneur_create_project, name='entrepreneur_create_project'),
    path('entrepreneur/projects/edit/<int:project_id>/', entrepreneur_edit_project, name='entrepreneur_edit_project'),
    path('entrepreneur/projects/delete/<int:project_id>/', entrepreneur_delete_project, name='entrepreneur_delete_project'),
    path('entrepreneur/generate_report/', entrepreneur_generate_report, name='entrepreneur_generate_report'),
   
    #investor area
    path('investor/dashboard/', investor_dashboard, name='investor_dashboard'),



    #test chart
    path('test-chart/', views.test_chart, name='test_chart'),
    
]


