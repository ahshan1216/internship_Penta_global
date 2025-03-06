from django.shortcuts import render ,redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'credential/login.html')

def signup(request):
    message = ""
    if request.method == 'POST':
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
            
            
    else:
        form = SignupForm()
        
    return render(request, 'credential/signup.html', {'form': SignupForm(), 'message': message})

def login(request):
    message = ""
    if request.method == 'POST':
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
    else:
        form = LoginForm()
        
    return render(request, 'credential/login.html', {'form': LoginForm(), 'message': message})