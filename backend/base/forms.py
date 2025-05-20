from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)
    phone = forms.CharField(max_length=20, required=True)
    user_type = forms.ChoiceField(choices=User.UserType.choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                 'phone', 'user_type', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user

class adminRegisterForm(forms.ModelForm):
    class Meta:
        model = admin
        fields = '__all__'

class EntrepreneurRegisterForm(forms.ModelForm):
    class Meta:
        model = Entrepreneur
        fields = '__all__'

class InvestorRegisterForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = '__all__'

class EntrepreneurForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '+1234567890'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.UserType.ENTREPRENEUR
        if commit:
            user.save()
        return user

class InvestorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '+1234567890'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.UserType.INVESTOR
        if commit:
            user.save()
        return user

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'goal_amount', 'deadline', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'goal_amount': forms.NumberInput(attrs={'min': 0}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'category': 'Catégorie',
            'goal_amount': 'Montant cible',
            'deadline': 'Date limite',
            'image': 'Image du projet',
        }
    def save(self, commit=True):
        project = super().save(commit=False)
        # Removed assignment to project.user because Project model has no 'user' attribute
        if commit:
            project.save()
        return project
