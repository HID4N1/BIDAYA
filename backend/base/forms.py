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

class EntrepreneurRegisterForm(forms.ModelForm):
    class Meta:
        model = Entrepreneur
        fields = []

class InvestorRegisterForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = []