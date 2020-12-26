from django.db import models
from projects.models import Project

role_options = [
    ('admin', 'Admin'),
    ('project manager', 'Project Manager'),
    ('developer', 'Developer')
]

# Create your models here.
class User(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.CharField(max_length=25)
    username = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=15)
    role = models.CharField(max_length=15)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    #set project foreign key to null initially when a user is first created
