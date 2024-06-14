from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:id>/',views.userProfile,name='user-profile'),


    path('login', views.loginUser, name='login'),
    path('logout',views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),
    path('account',views.userAccount, name='account'),
    path('edit-account',views.editAccount, name='account-form'),
    path('add-skill/',views.addSkill, name='add-skill'),
    path('edit-skill/<str:id>/',views.editSkill, name='edit-skill'),
    path('delete-skill/<str:id>/',views.deleteSkill, name='delete-skill'),
    path('inbox', views.inbox, name='inbox'),
    path('message/<str:id>/', views.message, name='message'),
    path('send-message/<str:id>/', views.sendMessage, name='send-message'),
]