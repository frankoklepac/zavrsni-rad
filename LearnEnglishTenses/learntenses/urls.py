from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('landing/', views.landing, name='landing'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('<str:tense_name>/tasks', views.task_list, name='task_list'),
    path('<str:tense>/task/<int:task_id>', views.task_detail, name='task_detail'),
]