from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from .forms import UserRegisterForm, UserProfileEditForm, UserEditForm, TaskForm
from .models import UserProfile, Task, UserTask
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from django.db import IntegrityError


def index(request):
    return render(request, 'learntenses/homepage.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            age = form.cleaned_data.get('age')
            new_user.userprofile.age = age
            new_user.userprofile.save()
            tasks = Task.objects.all()
            for task in tasks:
                UserTask.objects.create(user=new_user.userprofile, task=task) 
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

def task_list(request, tense_name):
    tense_mapping = {
        'present_simple': 'PS',
        'present_continuous': 'PC',
        'present_perfect': 'PP',
        'past_simple': 'PaS',
        'past_continuous': 'PaC',
        'past_perfect': 'PaP',
        'future_simple': 'FS',
        'future_continuous': 'FC',
        'future_perfect': 'FP',
    }
    tense_name_mapping = {
        'present_simple': 'Present Simple',
        'present_continuous': 'Present Continuous',
        'present_perfect': 'Present Perfect',
        'past_simple': 'Past Simple',
        'past_continuous': 'Past Continuous',
        'past_perfect': 'Past Perfect',
        'future_simple': 'Future Simple',
        'future_continuous': 'Future Continuous',
        'future_perfect': 'Future Perfect',
    }
    tense = tense_mapping.get(tense_name)
    tasks = Task.objects.filter(tense=tense).order_by('name')  
    user_profile = UserProfile.objects.get(user=request.user)
    user_tasks = list(UserTask.objects.filter(user=user_profile, task__in=tasks).order_by('task__name'))
    if user_tasks:
        user_tasks[0].locked = False 
        for i in range(1, len(user_tasks)):
            user_tasks[i].locked = not user_tasks[i-1].completed
    return render(request, 'learntenses/task_list.html', {'tasks': tasks, 'user_tasks': user_tasks, 'tense_name': tense_name_mapping.get(tense_name)})

def replace_with_span(sentence):
    words = sentence.split()
    for i, word in enumerate(words):
        if '<>' in word:
            words[i] = word.replace('<>', '<span class="blank" style="font-weight: bold;">_____</span>')
    return ' '.join(words)

@csrf_exempt
@require_http_methods(['GET','POST'])
def task_detail(request, tense, task_id):
    task = get_object_or_404(Task, id=task_id, tense=tense)
    user_profile = UserProfile.objects.get(user=request.user)
    user_task = get_object_or_404(UserTask, user=user_profile, task=task)
    task.sentence = replace_with_span(task.sentence)
    previous_task = Task.objects.filter(id__lt=task_id, tense=tense).order_by('-id').first()

    if not user_task.completed and (previous_task is not None and not UserTask.objects.filter(user=user_profile, task=previous_task, completed=True).exists()):
        return HttpResponseForbidden()

    return render(request, 'learntenses/task_detail.html', {'task': task, 'user_task': user_task, 'attempts_reached' : user_task.check_attempts()})

@csrf_exempt
def increment_attempts(request, task_id):
    user_profile = UserProfile.objects.get(user=request.user)
    task = get_object_or_404(Task, id=task_id)
    user_task = get_object_or_404(UserTask, user=user_profile, task=task)

    user_task.attempts += 1
    user_task.save()

    attempts_reached = user_task.check_attempts()

    return JsonResponse({'status': 'success', 'attempts_reached': attempts_reached})

@csrf_exempt
def reset_attempts(request, task_id):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_task = UserTask.objects.get(user=user_profile, task_id=task_id)
            user_task.reset_attempts()
            return JsonResponse({'status': 'success'})
        except UserTask.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'UserTask not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
@require_POST
def mark_as_completed(request, task_id):
    user_task = get_object_or_404(UserTask, user=request.user.userprofile, task_id=task_id)
    user_task.mark_as_completed()
    return JsonResponse({'status': 'success'})

def create_task(request):
    tasks = Task.objects.all()
    tenses = {choice[0]: [] for choice in Task.TENSE_CHOICES}
    for task in tasks:
        tenses[task.tense].append(task)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('home:create_task')
            except IntegrityError:
                form.add_error(None, 'A task with this name already exists for this tense')

    else:
        form = TaskForm()
    return render(request, 'learntenses/create_task.html', {'form': form, 'tenses':tenses})

def manage_tasks(request):
    tasks = Task.objects.all()
    tenses = {choice[0]: [] for choice in Task.TENSE_CHOICES}

    present_tenses = ['PS', 'PC', 'PP']
    past_tenses = ['PaS', 'PaC', 'PaP']
    future_tenses = ['FS', 'FC', 'FP']

    for task in tasks:
        tenses[task.tense].append(task)
    return render(request, 'learntenses/manage_tasks.html', {'tenses': tenses, 'present_tenses': present_tenses, 'past_tenses': past_tenses, 'future_tenses': future_tenses})

@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home:create_task')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home:manage_tasks')
    else:
        form = TaskForm(instance=task)

    tense_mapping = {
        'PS': 'Present Simple',
        'PC': 'Present Continuous',
        'PP': 'Present Perfect',
    }

    full_tense = tense_mapping.get(task.tense, task.tense)

    return render(request, 'learntenses/edit_task.html', {'form': form, 'full_tense': full_tense})

def learn_tense(request, tense_name):
    template_name = f'learntenses/learn_{tense_name}.html'
    return render(request, template_name)