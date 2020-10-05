from django.db import models
from django.contrib.auth import get_user_model

from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count

# to calculate current amount pledged on Project serializer
from django.db.models import Avg, Count, Min, Sum

class ProjectCategory(models.Model):
    name = models.CharField(max_length=80)

    # def __str__(self):
    #     return self.name
    

class Location(models.Model):
    name = models.CharField(max_length=200)
    # slug_name = models.CharField(max_length=50)

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
    view_count = models.IntegerField(default=3, blank=True)
    pledge_count = models.IntegerField(default=1, blank=True)

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
#         {
#             "amount": 50,
#             "comment": "LOVE this idea!! My dog is the worst driver. It's unbelievable that she's allowed behind the wheel without lessons.",
#             "anonymous": true,
#             "project_id": 1,
#             "date_created": "2020-08-19T23:30:58.401674Z",
#             "type_id": 3
#         }
#     ]
# }

# {
# "content": "Hi Everyone, quick update - we have changed the meeting point to the car park at Curtin Rowing Club. Just watch out for kids and dogs - it's a busy area by the playground and we don't want any accidents before you even get to start your driving lessons!"
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


# {
#     "title": "Creating new project TEST #1",
#     "description": "Is your dog a menace on the road? We are raising money to provide free driving classes to all dogs living in the City of South Perth. Term One will cover accelerating, braking and reverse-parallel parking. Treats will be provided, cars will not - each dog must have permission to learn in their owner's car. Let's make our neighborhood streets the safest in the metro area!.",
#     "goal_amount": 7500,
#     "image": "https://images.unsplash.com/photo-1561037404-61cd46aa615b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
#     "due_date": "2020-03-20T14:28:23.382748Z",
#     "category_id": 1
# }

# {
#         "title": "Music on the Foreshore",
#         "venue": "",
#         "description": "Pledge to come down and play music on the riverbank on a Saturday afternoon. Each set can last between 30 and 60 minutes. Bands and solo artists.",
#         "goal_amount": 2200,
#         "image": "https://images.unsplash.com/photo-1561037404-61cd46aa615b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
#         "due_date": "2020-03-20T14:28:23.382748Z",
#         "category_id": 3
#     },
    # {
    #     "title": "Cat Fishing Group",
    #     "venue": "Curtin Rowing Club",
    #     "description": "Do you know a cat that spends too much time on the internet using fake social media accounts to stalk their exes? We are encouraging all neighborhood cats to learn real fishing. They'll get some much-needed outdoor time and learn how to catch their own food!",
    #     "goal_amount": 750,
    #     "image": "https://images.unsplash.com/photo-1561037404-61cd46aa615b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
    #     "due_date": "2020-03-20T14:28:23.382748Z",
    #     "category": 1,
    #     "pledgetype": 1
    # }

# {
#         "amount": 75,
#         "comment": "LOVE this idea!! My dog is the worst driver. It's unbelievable that she's allowed behind the wheel without lessons.",
#         "anonymous": true
#     },
    # {
    #     "id": 2,
        # "amount": 75,
        # "comment": "YES yes yes. i LOVE driving.",
        # "anonymous": false,
    #     "user": 2,
    #     "project_id": 1,
    #     "date_created": "2020-08-25T13:50:17.201660Z",
    #     "type_id": 2
    # },
    # {
    #     "id": 5,
    #     "amount": 500,
    #     "comment": "Genius!",
    #     "anonymous": true,
    #     "user": 5,
    #     "project_id": 1,
    #     "date_created": "2020-08-29T10:52:43.369387Z",
    #     "type_id": 2
    # },


    # {
    #     "id": 1,
    #     "is_admin": true,
    #     "username": "michelle",
    #     "email": "mich@email.com",
    #     "location_id": 1,
    #     "password": "test4321",
    #     "favourite_categories": [
    #         1
    #     ]
    # },
    # {
    #     "id": 2,
    #     "is_admin": false,
    #     "username": "evie",
    #     "email": "evie@email.com",
    #     "location_id": 1,
    #     "favourite_categories": []
    # }
    #   {
    #     "id": 5,
    #     "is_admin": false,
    #     "username": "billy",
    #     "email": "billy@email.com",
    #     "location_id": 1,
    #     "favourite_categories": []
    # }
    #    {
    #     "id": 1,
    #     "date_posted": "2020-08-26T10:23:34.701803Z",
    #     "content": "Hey everyone! Here's an update on our project."
    #     }

    #         {
    #     "id": 1,
    #     "name": "Education"
    # },
    # {
    #     "id": 3,
    #     "name": "Arts"
    # },
    # {
    #     "id": 4,
    #     "name": "Natural Landscape"
    # },
    # {
    #     "id": 5,
    #     "name": "Kids"
    # }


# {
#   "content": "Hey everyone! Here's an update on our project. We've been in talks with Uber - they're interested in getting household pets into the gig economy and have offered to supply the dentasticks for afternoon tea.",
# "image": "https://images.unsplash.com/photo-1593297858385-1fa0a686f544?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80"
# }

# {
#     "title": "Doggy Driving Lessons",
#     "description": "Is your dog a menace on the road? We are raising money to provide free driving classes to all dogs living in the City of South Perth. Term One will cover accelerating, braking and reverse-parallel parking. Treats will be provided, cars will not - each dog must have permission to learn in their owner's car. Let's make our neighborhood streets the safest in the metro area!.",
#     "goal_amount": 7500,
#     "image": "https://images.unsplash.com/photo-1561037404-61cd46aa615b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
#     "is_open": true,
#     "due_date": "2020-09-17T14:28:23.382748Z",
#     "category": 1,
# "pledgetype": 1,
# "last_chance_triggered": false
# }
