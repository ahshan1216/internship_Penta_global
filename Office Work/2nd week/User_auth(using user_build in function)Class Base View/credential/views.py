from django.shortcuts import render ,redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.views import View

# Create your views here.

def home(request):
    return render(request, 'credential/login.html')


class SignupView(View):
    template_name = 'credential/signup.html'
    
    def get(self, request):
        return render(request, self.template_name, {'form': SignupForm()})
       
    def post(self,request):
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
                
            user=User.objects.create_user(username=username, email=email, password=password)
            user.save()
                
            message = "User created successfully"
            return redirect('login')  
        else:
            message = "Form is not valid"
                       
        return render(request, self.template_name, {'form': SignupForm(), 'message': message})

class LoginView(View):
    template_name = 'credential/login.html'
    
    def get(self, request):
        return render(request, self.template_name, {'form': LoginForm()})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
                
            user = User.objects.get(email=email)
            if user.check_password(password):
                message = "Login successful"
            else:
                message = "Login failed"
        else:
            message = "Form is not valid"

            
        return render(request, self.template_name, {'form': LoginForm(), 'message': message})
    
