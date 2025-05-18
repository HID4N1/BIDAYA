#urls set up

from django.urls import path
from .views import *


urlpatterns = [
    path('', Home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('projects/', projects, name='projects'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('redirect/', role_redirect, name='role_redirect'),
    
    #admin area
    path('Myadmin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('Myadmin/entrepreneurs/', admin_entrepreneurs, name='admin_ENT'),
    path('Myadmin/investors/', admin_investors, name='admin_INV'),
    path('Myadmin/notifications/', admin_notifications, name='admin_NOTIF'),
    path('Myadmin/analytics/', admin_analytics, name='admin_analytics'),
    #entrepreneur area
    path('entrepreneur/dashboard/', entrepreneur_dashboard, name='entrepreneur_dashboard'),

    #investor area
    path('investor/dashboard/', investor_dashboard, name='investor_dashboard'),


    
]


