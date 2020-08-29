from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/favourites/', views.ProjectListFiltered.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('projects/<int:project_pk>/progress-updates/', views.ProgressUpdateList.as_view()), 
    path('projects/<int:project_pk>/progress-updates/<int:update_pk>/', views.ProgressUpdateDetail.as_view()),
    path('projects/<int:project_pk>/pledges/', views.PledgeList.as_view()),
    path('projects/<int:project_pk>/pledges/<int:pledge_pk>/', views.PledgeDetail.as_view()),
    path('locations/<int:pk>/projects/', views.ProjectListByLocation.as_view()),
    path('project-categories/', views.ProjectCategoryList.as_view()),
    path('locations/<int:loc_pk>/categories/<int:cat_pk>/projects/', views.ProjectListByLocationAndCategory.as_view()),
    path('locations/', views.LocationList.as_view()),
    path('locations/<int:pk>/', views.LocationDetail.as_view()),    
    path('locations/<int:pk>/activity/', views.LocationActivity.as_view()),    
    path('project-categories/<int:pk>/', views.ProjectCategoryDetail.as_view()),
    
    # not using this url with slug below. Probably don't need to make it nice cos user won't see it I don't think - react should have it's own routes on the front end that the user sees...??
    # path('<str:location>/projects', views.LocationSLUGDetail.as_view()),

    # all paths below == admin only..??...
    path('pledges/types/', views.PledgetypeList.as_view()),
    path('pledges/types/<int:pk>/', views.PledgetypeDetail.as_view()),    
    
    # EXPERIMENTAL...
    path('activities/', views.AllActivity.as_view()),
    
] 

urlpatterns = format_suffix_patterns(urlpatterns)