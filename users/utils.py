from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProfiles(request):
    search_query = ''
    get_query =request.GET.get('search_query')
    if get_query:
        search_query = get_query
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(intro__icontains=search_query) |
        Q(skill__in=skills)
        )
    return profiles, search_query


def paginateProfiles(request, profiles, count):
    page = request.GET.get('page')
    paginator =Paginator(profiles,count)
    try:
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    if page == None:
        page = 1
    leftIndex = int(page) -4
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page)+5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1
    
    custom_range = range(leftIndex, rightIndex,)
    return custom_range, profiles