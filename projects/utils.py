from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProjects(request):
    search_query = ''
    get_query =request.GET.get('search_query')
    if get_query:
        search_query = get_query
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(tags__in=tags)
        )
    return projects, search_query


def paginateProjects(request, projects, count):
    projectsCount = count
    page = request.GET.get('page')
    paginator =Paginator(projects,projectsCount)
    try:
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    if page == None:
        page = 1
    leftIndex = int(page) -4
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page)+5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1
    
    custom_range = range(leftIndex, rightIndex,)
    return custom_range, projects