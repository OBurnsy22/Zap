from django.db import models
from projects.models import Project
from core.models import User
from django.core.files.storage import FileSystemStorage

# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=15, default="Open")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    priority = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True, blank=True)

#not working, fix later
class ticketHistory(models.Model):
    changed_property = models.CharField(max_length=30)
    old_value = models.CharField(max_length=30)
    new_value = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)

class ticketFile(models.Model):
    description = models.CharField(max_length=30)
    file = models.FileField()
    file_title = models.CharField(max_length=20, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
