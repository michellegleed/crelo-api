from django.db import models


class ProjectCategory(models.Model):
    name = models.CharField(max_length=80)
    
class Location(models.Model):
    name = models.CharField(max_length=200)
    # slug_name = models.CharField(max_length=50)

class Pledgetype(models.Model):
    type = models.CharField(max_length=50)

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    category = models.ForeignKey('ProjectCategory', on_delete=models.PROTECT)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='pledges')
    date_created = models.DateTimeField(auto_now_add=True)
    supporter = models.CharField(max_length=200)
    type = models.ForeignKey('Pledgetype', on_delete=models.PROTECT, related_name='pledgetype')



# {
#     "title": "project1",
#     "description": "description goes here",
#     "goal": "100",
#     "image": "https://images.unsplash.com/photo-1561037404-61cd46aa615b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
#     "is_open": "True",
#     "date_created": "2020-03-20T14:28:23.382748Z",
#     "creator": "michelle",
#     "due_date": "2020-03-20T14:28:23.382748Z"
# }

#  {
#     "amount": "50",
#     "comment": "I support this!!",
#     "anonymous": "True",
#     "supporter": "anonymous",
#     "project_id": "1",
#     "type_id": "3"
# }