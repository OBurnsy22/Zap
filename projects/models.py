from django.db import models


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=300)
    #ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    #with project fields, when they click details, list assigned
    #users, as well as all tickets assigned to this project
