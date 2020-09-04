from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetail.as_view()),
    path('account/', views.AuthenticatedUserProfile.as_view()),
    path('account/add-category/<pk>/', views.UserAddCategory.as_view()),
    path('account/remove-category/<pk>/', views.UserRemoveCategory.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)