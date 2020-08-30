from django.db import models
from django.contrib.auth import get_user_model


class ProjectCategory(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.username
    

class Location(models.Model):
    name = models.CharField(max_length=200)
    # slug_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name        


class Pledgetype(models.Model):
    type = models.CharField(max_length=50)


class ProgressUpdate(models.Model):
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='updates')
    date_posted = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    

class Project(models.Model):
    title = models.CharField(max_length=200)
    venue = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    goal_amount = models.IntegerField()
    current_amount = models.IntegerField(default=0, blank=True)
    image = models.URLField()
    is_open = models.BooleanField(default=True, blank=True)
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
    next_milestone = models.IntegerField(default=25, blank=True)


class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project', 
        on_delete=models.CASCADE, 
        related_name='pledges'
    )
    date_created = models.DateTimeField(auto_now_add=True)
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

# Activity possible actions: 
    # - project reaches goal amount (and 25%, 50% and 100%)
    # - creator posts a progress update
    # - someone comments on a project you've pledged to'
    # - new project created


class Activity(models.Model):
    action = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    object_model = models.CharField(max_length=100)
    object_id = models.IntegerField()
    
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
    

# SHELL COMMANDS #
# from projects.models import Project
# Project.objects.all()
# pj = Project.objects.get(pk=)
# pj.delete()


# {
#     "title": "Doggy Driving Lessons",
#     "description": "Is your dog a menace on the road? We are raising money to provide free driving classes to all dogs living in the City of South Perth. Term One will cover accelerating, braking and reverse-parallel parking. Treats will be provided, cars will not - each dog must have permission to learn in their owner's car. Let's make our neighborhood streets the safest in the metro area!.",
#     "goal": 7500,
#     "image": "https://images.unsplash.com/photo-1561037404-61cd46aa615b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
#     "is_open": true,
#     "date_created": "2020-08-19T22:41:43.180006Z",
#     "due_date": "2020-03-20T14:28:23.382748Z",
#     "category_id": 1,
#     "location_id": 1,
#     "pledges": [
        # {
        #     "amount": 50,
        #     "comment": "LOVE this idea!! My dog is the worst driver. It's unbelievable that she's allowed behind the wheel without lessons.",
        #     "anonymous": true,
        #     "project_id": 1,
        #     "date_created": "2020-08-19T23:30:58.401674Z",
        #     "type_id": 3
        # }
#     ]
# }

# {
    # "username": "ruby",
    # "email": "ruby@gmail.com",
    # "password": "test4321",
    # "location_id": 2
# }

# {
# "amount": 55,
# "comment": "woohoo! triggered another milestone!",
# "anonymous": false,
# "type_id": 2
# }