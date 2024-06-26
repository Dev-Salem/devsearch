from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('',views.getRoutes,),
    path('projects/', views.getProjects),
    path('project/<str:id>/', views.getProject),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/<str:id>/vote/', views.projectVote, ),
    path('remove-tag/', views.removeTag),
]