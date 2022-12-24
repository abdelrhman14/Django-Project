from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(Q(email__iexact=email)).exists():
            raise forms.ValidationError('Email is already exist')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(Q(username__iexact=username)).exists():
            raise forms.ValidationError('Username is already exist please try again')
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError("Password don't match")

        return password2

class UserForm(forms.ModelForm):
   
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','country','address','ph_number']
