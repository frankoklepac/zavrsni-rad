from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Task

class UserRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'age']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, name=self.cleaned_data["name"], age=self.cleaned_data["age"])
        return user

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'age']

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        self.label_suffix = "" 

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.label_suffix = "" 

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['level', 'tense', 'name', 'sentence', 'words', 'correct_words']