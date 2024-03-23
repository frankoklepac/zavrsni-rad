from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Task(models.Model):
    TENSE_CHOICES = [
        ('PS', 'Present Simple'),
        ('PC', 'Present Continuous'),
        ('PP', 'Present Perfect'),
        ('PaS', 'Past Simple'),
        ('PaC', 'Past Continuous'),
        ('PaP', 'Past Perfect'),
        ('FS', 'Future Simple'),
        ('FC', 'Future Continuous'),
        ('FP', 'Future Perfect'),
    ]
    TASK_LEVELS = [
        ('1', 'Task 1'),
        ('2', 'Task 2'),
        ('3', 'Task 3'),
        ('4', 'Task 4'),
        ('5', 'Task 5'),
        ('6', 'Task 6')
    ]
    tense = models.CharField(max_length=3, choices=TENSE_CHOICES)
    name = models.CharField(max_length=10, choices=TASK_LEVELS)
    sentence = models.CharField(max_length=500)
    words = models.CharField(max_length=500)
    correct_words = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.get_tense_display()} - {self.get_name_display()}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs) 
        if is_new:
            for user_profile in UserProfile.objects.all():
                UserTask.objects.create(user=user_profile, task=self)

class UserTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    def __str__ (self):
        return f"{self.user} - {self.task}"