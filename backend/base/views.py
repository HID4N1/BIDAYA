
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
            return redirect('login')
    else:
        user_form = UserRegisterForm()
    
    return render(request, 'base/conexion/register.html', {'user_form': user_form})

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'base/conexion/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'ADM':  # Your custom admin
            return reverse_lazy('admin_dashboard')  # Your custom dashboard URL
        elif user.user_type == 'ENT':
            return reverse_lazy('entrepreneur_dashboard')
        elif user.user_type == 'INV':
            return reverse_lazy('investor_dashboard')
        return reverse_lazy('home')  # Fallback


def logout(request):
    auth_logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required


@login_required
def role_redirect(request):
    user = request.user
    if user.user_type == 'ADM':
        return redirect('admin_dashboard')
    elif user.user_type == 'ENT':
        return redirect('entrepreneur_dashboard')
    elif user.user_type == 'INV':
        return redirect('investor_dashboard')
    return redirect('home')  # Fallback for undefined roles

from .decorators import admin_required, entrepreneur_required, investor_required

# admin views
@admin_required
def admin_dashboard(request):
    return render(request, 'base/admin/admin_dashboard.html')

@admin_required
def admin_entrepreneurs(request):
    return render(request, 'base/admin/admin_ENT.html')

@admin_required
def admin_investors(request):
    return render(request, 'base/admin/admin_INV.html')

@admin_required
def admin_notifications(request):
    return render(request, 'base/admin/admin_NOTIF.html')

@admin_required
def admin_analytics(request):
    return render(request, 'base/admin/admin_analytics.html')

# entrepreneur views

@entrepreneur_required
def entrepreneur_dashboard(request):
    return render(request, 'base/entrepreneur/entrepreneur_dashboard.html')

# investor views

@investor_required
def investor_dashboard(request):
    return render(request, 'base/investisseur/investor_dashboard.html')