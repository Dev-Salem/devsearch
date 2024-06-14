from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth import login, authenticate, logout
from .models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth.decorators import *
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles
def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles =paginateProfiles(request, profiles, 3)
    context = {'profiles': profiles, 'search_query': search_query, "custom_range":custom_range}
    return render(request,'users/profiles.html', context)

def userProfile(request,id):
    profile = Profile.objects.get(id=id)
    topSkills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request,'users/user-profile.html', context)

def loginUser(request):
    page = 'login'
    context = {'page':page}
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username =request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=request.POST['username'])
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('projects')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    return render(request,'users/login-register.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.success(request,"Logout successfully")
    return redirect('login')

def registerUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User Account was created")
            login(request, user)
            return redirect('account-form')
        else:
            print(request.POST)
            messages.error(request,'Invalid data')

    page = 'register'
    form = CustomUserCreationForm()
    context = {'page':page, 'form':form}
    return render(request,'users/login-register.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    projects = profile.project_set.all()
    skills = profile.skill_set.all()
    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = AccountForm(instance=profile)

    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {"form":form}
    return render(request,'users/account-form.html',context)

@login_required(login_url='login')
def editSkill(request, id):
    profile =request.user.profile
    skill = profile.skill_set.get(id=id)
    form = SkillForm(instance=skill)
    if request.method=='POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            return redirect('account')
    context = {'form':form,}
    return render(request,'users/skill-form.html',context)

@login_required(login_url='login')
def addSkill(request):
    form = SkillForm()
    if request.method=='POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            return redirect('account')
    context = {'form':form,}
    return render(request,'users/skill-form.html',context)

@login_required(login_url='login')
def deleteSkill(request,id):
    skill = request.user.profile.skill_set.get(id=id)
    if request.method=='POST':
        skill.delete()
        return redirect('account')
    context = {"object":skill,}
    return render(request,'projects/delete-template.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    inboxMessages = profile.messages.all()
    unreadCount = inboxMessages.filter(is_read=False).count()
    print("================================")
    print(inboxMessages)
    context = {'inboxMessages':inboxMessages, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)


def message(request,id):
    profile = request.user.profile

    msg = profile.messages.get(id=id)
    if msg.is_read == False:
        msg.is_read = True
        msg.save()
    context = {'msg':msg}
    return render(request, 'users/message.html',context)


def sendMessage(request,id):
    if request.user.is_authenticated == False:
        messages.error(request, "Login First")
        return redirect('login')
    
    form = MessageForm()
    recipient = Profile.objects.get(id=id)
    if request.method == 'POST':
        form = MessageForm(request.POST,)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender =request.user.profile
            message.recipient =recipient
            message.is_read = False
            message.name = request.user.profile.name
            message.email = request.user.email

            message.save()
            return redirect('account')
    context = {'form':form, 'recipient':recipient}
    return render(request,'users/send-message.html',context) 