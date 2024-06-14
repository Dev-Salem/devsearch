from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import *
from django.contrib import messages
from django.db.models import Q
from .utils import searchProjects, paginateProjects
from django.db import IntegrityError

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    context = {'projects':projects, 'search_query':search_query,'custom_range':custom_range }
    return render(request, 'projects/projects.html', context)



def project(request, id):
    singleProject = Project.objects.get(id=id)
    form = ReviewForm()
    if request.method == 'POST':
        try:
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.owner = request.user.profile
            review.project = singleProject
            review.save()
            singleProject.updateVote
        except IntegrityError:
            messages.error(request, "Already wrote a review")

    context = {'project': singleProject, 'form':form}
    print(singleProject.reviewers)
    return render(request, 'projects/project.html', context)

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    context = {'form':form}
    newTags = request.POST.get('newtags').replace(',', ' ').split()
    if(request.method == 'POST'):
        form = ProjectForm(request.POST, request.FILES,)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag) 
            return redirect('projects')
    return render(request, 'projects/create-project.html', context)

@login_required(login_url='login')
def updateProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)
    if(request.method == 'POST'):
        newTags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag) 
            
            return redirect('account')
        else:
            messages.error(request,"Something went wrong")
    context = {'form':form, 'project':project}
    return render(request, 'projects/create-project.html', context)

@login_required(login_url='login')
def deleteProject(request, id):
    profile = request.user.profile
    project= profile.project_set.get(id=id)
    context = {'object':project}
    if(request.method == 'POST'):
        project.delete()
        return redirect('account')
    return render(request, 'projects/delete-template.html', context)


    
