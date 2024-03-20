from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from .forms import UserRegisterForm, UserProfileEditForm, UserEditForm
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def index(request):
    return render(request, 'learntenses/base.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home:login')
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
                auth_login(request, user)  
                return redirect('home:index')
            else:
                return redirect('home:login')
    else:  
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
    
def logout(request):
    auth_logout(request)
    return redirect('home:landing')

def landing(request):
    return render(request, 'learntenses/landing.html')

def profile(request):
    return render(request, 'learntenses/profile.html')

def edit_profile(request):
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user, age=0) 
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)
    return render(request, 'learntenses/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            return redirect('home:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'learntenses/change_password.html', {'form': form})