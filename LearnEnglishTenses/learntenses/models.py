from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
