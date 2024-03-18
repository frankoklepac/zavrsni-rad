from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from .forms import UserRegisterForm
# Create your views here.
def index(request):
    
    return render(request, 'learntenses/base.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration:login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('learntenses:base')
            else:
                return redirect('registration:register')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})