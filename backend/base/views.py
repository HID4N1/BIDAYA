
from django.views import View
from django.shortcuts import redirect, render
from .forms import *
from .models import *

# Create your views here.

def Home(request):
    return render(request, 'base/home.html')

def about(request):
    return render(request, 'base/about.html')

def contact(request):
    return render(request, 'base/contact.html')

def projects(request):
    return render(request, 'base/projects.html')

def login(request):
    return render(request, 'base/conexion/login.html')

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            
            if user.user_type == User.UserType.ENTREPRENEUR:
                Entrepreneur.objects.create(user=user)
            elif user.user_type == User.UserType.INVESTOR:
                Investor.objects.create(user=user)
            
            auth_login(request, user)
            return redirect('home')
    else:
        user_form = UserRegisterForm()
    
    return render(request, 'base/conexion/register.html', {'user_form': user_form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password."
            return render(request, 'base/conexion/login.html', {'error_message': error_message})
    else:
        return render(request, 'base/conexion/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required

def admin_area(request):
    if request.user.is_authenticated and request.user.user_type == User.UserType.ADMIN:
        return render(request, 'base/admin_dashboard.html')
    else:
        return redirect('home')
