from django.db import models
from django.contrib.auth.models import AbstractUser

from projects.models import ProjectCategory, Location

class CustomUser(AbstractUser):

    def __str__(self):
        return self.username
