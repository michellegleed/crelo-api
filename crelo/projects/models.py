from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField()
    creator = models.CharField(max_length=200)
    due_date = models.DateTimeField()

class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
        )
    supporter = models.CharField(max_length=200)


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
#     "id": "1",
#     "amount": "50",
#     "comment": "I support this!!",
#     "anonymous": "True",
#     "supporter": "anonymouse",
#     "project_id": "1"
# }