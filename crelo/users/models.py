from django.db import models
from django.contrib.auth.models import AbstractUser

from projects.models import ProjectCategory, Location

class CustomUser(AbstractUser):
    location = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        related_name='user_location'
    )
    bio = models.TextField(blank=True, default="")
    image = models.URLField(blank=True, default="")
    is_admin = models.BooleanField(blank=True, default=False)
    favourite_categories = models.ManyToManyField(ProjectCategory, related_name='customuser', blank=True)

    def __str__(self):
        return self.username
