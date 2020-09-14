from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class MembershipInline(admin.TabularInline):
    model = CustomUser.favourite_topics.through
    

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_admin', 'location']
    inlines = [
        MembershipInline,
    ]

admin.site.register(CustomUser, CustomUserAdmin)

