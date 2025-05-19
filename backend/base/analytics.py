# base/analytics.py
from django.apps import apps
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.db.models.functions import TruncDate

def get_analytics_data():
    # Get models using apps.get_model to avoid AppRegistryNotReady
    User = apps.get_model('base', 'User')
    Project = apps.get_model('base', 'Project')
    Investment = apps.get_model('base', 'Investment')  # Assuming you have this model
    Donation = apps.get_model('base', 'Donation')    # Assuming you have this model

    # Calculate time ranges
    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    last_12_months = now - timedelta(days=365)

    # User analytics
    entrepreneurs = User.objects.filter(user_type=User.UserType.ENTREPRENEUR)
    investors = User.objects.filter(user_type=User.UserType.INVESTOR)
    
    # Project analytics
    projects = Project.objects.all()
    completed_projects = projects.filter(status='COMPLETED')
    pending_projects = projects.filter(status='PENDING')

    # Financial analytics
    total_investment = Investment.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_donation = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_revenue = total_investment + total_donation

    # Time-based data for charts
    monthly_users = User.objects.filter(
        date_joined__gte=last_30_days
    ).annotate(
        date=TruncDate('date_joined')
    ).values('date').annotate(
        entrepreneurs=Count('id', filter=models.Q(user_type=User.UserType.ENTREPRENEUR)),
        investors=Count('id', filter=models.Q(user_type=User.UserType.INVESTOR))
    ).order_by('date')

    revenue_sources = [
        {'source': 'Investment', 'amount': total_investment},
        {'source': 'Donation', 'amount': total_donation}
    ]




    return {
        'total_entrepreneurs': entrepreneurs.count(),
        'total_investors': investors.count(),
        'total_projects': projects.count(),
        'completed_projects': completed_projects.count(),
        'pending_projects': pending_projects.count(),
        'total_revenue': total_revenue,
        'monthly_users': list(monthly_users),
        'revenue_sources': revenue_sources, 
        # Add more analytics data as needed
    }
