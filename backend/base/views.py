from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from .models import *


# Create your views here.

def Home(request):
    context = {
        'title': 'Home | BIDAYA',
    }
    return render(request, 'base/home.html', context)

def about(request):
    context = {
        'title': 'About | BIDAYA',
    }
    return render(request, 'base/about.html', context)

def contact(request):
    context = {
        'title': 'Contact | BIDAYA',
    }
    return render(request, 'base/contact.html', context)

def projects(request):
    context = {
        'title': 'Projects | BIDAYA',
    }
    return render(request, 'base/projects.html', context)

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

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class CustomLoginView(LoginView):
    template_name = 'base/conexion/login.html'
    authentication_form = AuthenticationForm

    def form_invalid(self, form):
        # Called when the form is invalid (e.g., wrong credentials)
        return self.render_to_response(self.get_context_data(form=form, error="Invalid username or password."))

    def form_valid(self, form):
        # Log the user in
        auth_login(self.request, form.get_user())
        return super().form_valid(form)

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
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum

# admin views
@admin_required
def admin_dashboard(request):

    num_entrepreneurs = User.objects.filter(user_type=User.UserType.ENTREPRENEUR).count()
    num_investors = User.objects.filter(user_type=User.UserType.INVESTOR).count()
    num_projects = Project.objects.count()
    total_revenue = Project.objects.aggregate(Sum('current_amount'))['current_amount__sum'] or 0
    context = {
        'num_entrepreneurs': num_entrepreneurs,
        'num_investors': num_investors,
        'num_projects': num_projects,
        'Total_revenue': total_revenue,
    }
    return render(request, 'base/admin/admin_dashboard.html', context)

@admin_required
def admin_entrepreneur(request):
    entrepreneur_users = User.objects.filter(user_type=User.UserType.ENTREPRENEUR).select_related('entrepreneur')
    context = {
        'title': 'Entrepreneurs | BIDAYA',
        'entrepreneur_users': entrepreneur_users,
    }
    return render(request, 'base/admin/admin_ENT.html', context)

@admin_required
def edit_entrepreneur(request, entrepreneur_id):
    user = get_object_or_404(User, id=entrepreneur_id, user_type=User.UserType.ENTREPRENEUR)
    if request.method == 'POST':
        form = EntrepreneurForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrepreneur modifié avec succès!")
            return redirect('admin_ENT')
    else:
        form = EntrepreneurForm(instance=user)
    return render(request, 'base/admin/edit_entrepreneur.html', {'form': form, 'user': user})

@admin_required
def delete_entrepreneur(request, entrepreneur_id):
    user = get_object_or_404(User, id=entrepreneur_id, user_type=User.UserType.ENTREPRENEUR)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_ENT')
    return render(request, 'base/admin/confirm_delete.html', {'entrepreneur': user})


@admin_required
def admin_investors(request):
    investor_users = User.objects.filter(user_type=User.UserType.INVESTOR).select_related('investor')
    context = {
        'title': 'Investors | BIDAYA',
        'investor_users': investor_users,
    }
    return render(request, 'base/admin/admin_INV.html', context)

@admin_required
def edit_investor(request, investisseur_id):
    user = get_object_or_404(User, id=investisseur_id)
    if request.method == 'POST':
        form = InvestorForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Investor modifié avec succès!")
            return redirect('admin_INV')
    else:
        form = InvestorForm(instance=user)
    return render(request, 'base/admin/edit_investor.html', {'form': form, 'user': user})

@admin_required
def delete_investor(request, investisseur_id):
    user = get_object_or_404(User, id=investisseur_id, user_type=User.UserType.INVESTOR)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_INV')
    return render(request, 'base/admin/confirm_delete.html', {'investor': user})

@admin_required
def admin_notifications(request):
    return render(request, 'base/admin/admin_NOTIF.html')
    
    
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils.timezone import now
from datetime import timedelta

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .decorators import admin_required

@admin_required
def admin_generate_report(request):
    # Gather data
    num_entrepreneurs = User.objects.filter(user_type=User.UserType.ENTREPRENEUR).count()
    num_investors = User.objects.filter(user_type=User.UserType.INVESTOR).count()
    num_projects = Project.objects.count()
    total_revenue = Project.objects.aggregate(Sum('current_amount'))['current_amount__sum'] or 0

    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admin_report.pdf"'

    # Create the PDF object, using the response as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(72, height - 72, "Admin Dashboard Report")

    # Data
    p.setFont("Helvetica", 12)
    p.drawString(72, height - 108, f"Total Entrepreneurs: {num_entrepreneurs}")
    p.drawString(72, height - 132, f"Total Investors: {num_investors}")
    p.drawString(72, height - 156, f"Total Projects: {num_projects}")
    p.drawString(72, height - 180, f"Total Revenue: ${total_revenue:.2f}")

    # Finish up
    p.showPage()
    p.save()
    return response





from .analytics import get_analytics_data
import json
from django.db.models import Count
from django.db.models import Sum
@admin_required
def admin_analytics(request):
    from .analytics import get_analytics_data

    analytics_data = get_analytics_data()

    monthly_users = analytics_data.get('monthly_users', [])
    # Convert date objects to string for JSON serialization
    for entry in monthly_users:
        if 'date' in entry and hasattr(entry['date'], 'isoformat'):
            entry['date'] = entry['date'].isoformat()

    monthly_users_json = json.dumps(monthly_users)
    total_projects = analytics_data.get('total_projects', 0)
    completed_projects = analytics_data.get('completed_projects', 0)
    pending_projects = analytics_data.get('pending_projects', 0)
    active_projects = total_projects - completed_projects - pending_projects

    # Convert Decimal to float for JSON serialization
    total_revenue = float(analytics_data.get('total_revenue', 0))
    total_investment = float(analytics_data.get('total_investment', 0))
    total_donation = float(analytics_data.get('total_donation', 0))

    context = {
        'title': 'Analytics | BIDAYA',
        'total_entrepreneurs': analytics_data.get('total_entrepreneurs', 0),
        'total_investors': analytics_data.get('total_investors', 0),
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'pending_projects': pending_projects,
        'active_projects': active_projects,
        'total_revenue': total_revenue,
        'total_investment': total_investment,
        'total_donation': total_donation,
        'monthly_users': monthly_users_json,
    }

    return render(request, "base/admin/admin_analytics.html", context)





# entrepreneur views
@entrepreneur_required
def entrepreneur_dashboard(request):
    return render(request, 'base/entrepreneur/entrepreneur_dashboard.html')

# investor views
@investor_required
def investor_dashboard(request):
    return render(request, 'base/investisseur/investor_dashboard.html')