from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    location_id = models.IntegerField() 
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
