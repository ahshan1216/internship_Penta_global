from django import forms
from django.contrib.auth.models import User

# Signup Form
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Hide password input

    class Meta:
        model = User
        fields = ["username", "email", "password"]  # Username is used for 'name'

# Login Form
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
