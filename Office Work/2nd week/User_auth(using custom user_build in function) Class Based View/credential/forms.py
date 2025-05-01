from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()
# Signup Form
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Hide password input
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)


    class Meta:
        model = User
        fields = ["username", "email", "password","role"]  # Username is used for 'name'

# Login Form
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
