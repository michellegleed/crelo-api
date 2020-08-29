from django.db import models
from django.contrib.auth.models import AbstractUser

from projects.models import ProjectCategory, Location

class CustomUser(AbstractUser):
    location = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        related_name='user_location'
    )
    is_admin = models.BooleanField(default=False)
    favourite_categories = models.ManyToManyField(ProjectCategory, related_name='customuser')

    def __str__(self):
        return self.username
