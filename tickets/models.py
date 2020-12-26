from django.db import models
from projects.models import Project
from core.models import User

# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=15, default="Open")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    priority = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True, blank=True)

class ticketHistory(models.Model):
    changed_property = models.CharField(max_length=30),
    old_value = models.CharField(max_length=30),
    new_value = models.CharField(max_length=30),
    date = models.DateTimeField(auto_now_add=True, blank=True),
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)






#For printing tickets related to a particular project, assign
#project a tickets is related to under the Ticket foreign key field,
#then when I need to populate a table with tickets for a project, just
#search through all tickets in database, cherrypicking the ones with the
#corresponding project you are referring to
