from django import forms
from .models import Teacher
from django.contrib.auth.models import User
from . import models

class SignInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'styled-input','id':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'styled-input','id':'password'}))

class addTeacherForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        error_messages = {
            'first_name': {'required': 'Please enter your first name'},
            'last_name': {'required': 'Please enter your last name'},
        }
# class Teacherform(forms.ModelForm):
#     class Meta:
#         model=models.Teacher
#         fields=['mobile']

# class SignUpForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['first_name', 'username', 'email', 'password']