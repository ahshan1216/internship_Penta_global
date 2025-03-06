from django.shortcuts import render


def home(request):
    return render(request, 'working_process/home.html')