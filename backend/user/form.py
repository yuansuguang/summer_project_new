from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    new_password1 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=254)

class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length=20, widget=forms.PasswordInput)

