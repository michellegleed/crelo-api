from django.db import models
from django.contrib.auth.models import AbstractUser

from projects.models import ProjectCategory

class CustomUser(AbstractUser):
    location_id = models.IntegerField() 
    is_admin = models.BooleanField(default=False)
    favourite_categories = models.ManyToManyField(ProjectCategory, related_name='customuser')

    def __str__(self):
        return self.username
