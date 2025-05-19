from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Permission


# Create your models here.

class User(AbstractUser):
    # Additional fields for the user model
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # User types
    class UserType(models.TextChoices):
        ENTREPRENEUR = 'ENT', 'Entrepreneur'
        INVESTOR = 'INV', 'Investor'
        ADMIN = 'ADM', 'Admin'
    
    user_type = models.CharField(
        max_length=3,
        choices=UserType.choices,
        default=UserType.INVESTOR
    )

    def save(self, *args, **kwargs):
        # First save to create the user
        super().save(*args, **kwargs)
        
        # Assign new permissions
        if self.user_type == self.UserType.ADMIN:
            self.is_staff = False  # remove admin access to Django admin 
            perm = Permission.objects.get(codename='is_admin')
        elif self.user_type == self.UserType.ENTREPRENEUR:
            perm = Permission.objects.get(codename='is_entrepreneur')
        elif self.user_type == self.UserType.INVESTOR:
            perm = Permission.objects.get(codename='is_investor')
        
        self.user_permissions.add(perm)

    class Meta:
        permissions = (
            ('is_entrepreneur', 'Can create projects'),
            ('is_investor', 'Can invest in projects'),
            ('is_admin', 'Can manage the platform'),
        )
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class admin(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.UserType.ADMIN}

    )
    def __str__(self):
        return f"Admin: {self.user.get_full_name()}"

class Entrepreneur(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.UserType.ENTREPRENEUR}
    )
    
    def __str__(self):
        return f"Entrepreneur: {self.user.get_full_name()}"
    
    def create_project(self, **kwargs):
        return Project.objects.create(creator=self, **kwargs)

class Investor(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.UserType.INVESTOR}
    )
    investment_history = models.TextField(blank=True)
    
    def __str__(self):
        return f"Investor: {self.user.get_full_name()}"

class Category(models.Model):
    """Event categories"""
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        ACTIVE = 'AC', 'Active'
        FUNDED = 'FU', 'Funded'
        COMPLETED = 'CO', 'Completed'
        CANCELLED = 'CA', 'Cancelled'
    
    creator = models.ForeignKey(
        Entrepreneur,
        on_delete=models.CASCADE,
        related_name='projects_created'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ManyToManyField(Category)
    goal_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    current_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    location = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    investors = models.ManyToManyField(
        Investor,
        through='Investment',
        related_name='projects_invested'
    )
    
    def __str__(self):
        return f"{self.title} by {self.creator.user.get_full_name()}"
    
    def add_investment(self, investor, amount):
        investment = Investment.objects.create(
            project=self,
            investor=investor,
            amount=amount
        )
        self.current_amount += amount
        self.save()
        return investment
    
    def update_status(self, new_status):
        self.status = new_status
        self.save()
    
    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE
    
    @property
    def days_remaining(self):
        return (self.deadline - timezone.now()).days if self.deadline else 0

class Media(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='media_files'
    )
    file = models.FileField(upload_to='project_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Media for {self.project.title}"

class Investment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.investor.user.get_full_name()} invested {self.amount} in {self.project.title}"

class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    donor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.donor.user.get_full_name()} donated {self.amount} to {self.project.title}"

class Payment(models.Model):
    investment = models.OneToOneField(
        Investment,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    
    def process_payment(self):
        # Implement payment processing logic
        self.is_completed = True
        self.save()
    
    def refund(self):
        # Implement refund logic
        self.is_refunded = True
        self.save()
    
    def __str__(self):
        return f"Payment #{self.transaction_id} for {self.investment}"
