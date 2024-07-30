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
    path('<str:tense_name>/learn', views.learn_tense, name='learn_tense'), 
    path('<str:tense_name>/tasks', views.task_list, name='task_list'),
    path('<str:tense>/task/<int:task_id>', views.task_detail, name='task_detail'),
    path('increment_attempts/<int:task_id>/', views.increment_attempts, name='increment_attempts'),
    path('mark_as_completed/<int:task_id>/', views.mark_as_completed, name='mark_as_completed'),
    path('reset_attempts/<int:task_id>/', views.reset_attempts, name='reset_attempts'),
    path('create_task/', views.create_task, name='create_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('manage_tasks/', views.manage_tasks, name='manage_tasks'),
]