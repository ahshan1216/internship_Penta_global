from django.shortcuts import render ,redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views import View
import datetime, jwt
from rest_framework.response import Response

# Create your views here.

def home(request):
    
    return render(request, 'credential/login.html' , {'form': LoginForm()})

User = get_user_model()


class SignupView(View):
    template_name = 'credential/signup.html'
    def get(self, request):
        return render(request, self.template_name , {'form': SignupForm()})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            user = User.objects.create_user(username=username, email=email, password=password, role=role)
            user.save()

            return redirect('login')
        else:
            return render(request, 'credential/signup.html', {'form': SignupForm()})


class LoginView(View):
    template_name = 'credential/login.html'
    
    def get(self, request):
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.filter(email=email).first()  
            if user:
                if user.check_password(password):
                    payload = {
                        'id': user.id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
                        'iat': datetime.datetime.utcnow()
                    }
                    token = jwt.encode(payload, 'secret', algorithm='HS256')
                    # return Response({'jwt': token})
                    return render(request, 'dashboard/dashboard.html', {'jwt_token': token})
                    # return redirect('dashboard')
                else:
                    message = "Invalid password"
            else:
                message = "User with this email does not exist"

            
        else:
            message = "Form is not valid"
            
        