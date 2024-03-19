from django import forms
from django.contrib.auth.models import User as AuthUser 
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    age = forms.IntegerField()

    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'password1', 'password2', 'name', 'age']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, name=self.cleaned_data["name"], age=self.cleaned_data["age"])
        return user