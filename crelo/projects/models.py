from django.db import models
from django.contrib.auth import get_user_model

from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count

# to calculate current amount pledged on Project serializer
from django.db.models import Avg, Count, Min, Sum

class ProjectCategory(models.Model):
    name = models.CharField(max_length=80)
    

class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name        


class Pledgetype(models.Model):
    type = models.CharField(max_length=50)
    

class Project(models.Model):
    title = models.CharField(max_length=200)
    venue = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    goal_amount = models.IntegerField()
    current_amount = models.IntegerField(default=0, blank=True)
    image = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        related_name='user_projects'
    )
    due_date = models.DateTimeField()
    category = models.ForeignKey(
        ProjectCategory, 
        on_delete=models.PROTECT, 
        related_name='category_projects'
    )
    location = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        related_name='location_projects')
    last_milestone = models.IntegerField(default=0, blank=True)
    pledgetype = models.ForeignKey(
        Pledgetype, 
        on_delete=models.PROTECT)
    # Need to keep track of this so the activity object for "last-chance" to pledge is only created once.
    last_chance_triggered = models.BooleanField(default=False, blank=True)
    view_count = models.IntegerField(default=0, blank=True)
    pledge_count = models.IntegerField(default=0, blank=True)

    @property
    def is_open(self):
        return self.due_date > now()
    
    @property
    def current_amount_pledged(self):
        current_amt = self.pledges.aggregate(value=Sum('amount'))
        return current_amt['value']

    @property
    def current_percentage_pledged(self):
        if self.current_amount_pledged:
            return round(self.current_amount_pledged / self.goal_amount * 100, 1)
        return 0


class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=400)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project', 
        on_delete=models.CASCADE, 
        related_name='pledges'
    )
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, 
        related_name='user_pledges'
    )
    type = models.ForeignKey(
        'Pledgetype', 
        on_delete=models.PROTECT, 
        related_name='pledgetype'
    )

class ProgressUpdate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image = models.URLField()

# Activity possible actions: 
    # - project reaches goal amount (and 25%, 50% and 75%)
    # - creator posts a progress update
    # - new project created
    # - last chance to pledge before closing - maybe @ 5 days to go.

class Activity(models.Model):
    action = models.CharField(max_length=200)
    info = models.TextField(4000)
    date = models.DateTimeField(auto_now_add=True)
    image = models.URLField()
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        related_name='user_activity'
    )
    location = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        related_name='location_activity'
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='project_activity'
    )
    
