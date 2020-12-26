from django import forms
from tickets.models import Ticket
from projects.models import Project

#ticket type choices
type_choices = [
    ('Feature Request', 'Feature Fequest'),
    ('Bug/Error', 'Bug/Error'),
    ('Comment', 'Comment')
]

#ticket priority choices
priority_choices = [
    ('None', 'None'),
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High')
]

status_choices = [
    ('Open', 'Open'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved'),
    ('Closed', 'Closed')
]

class ticketForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all().order_by('name'))
    type = forms.CharField(max_length=15, widget=forms.Select(choices=type_choices))
    priority = forms.CharField(max_length=15, widget=forms.Select(choices=priority_choices))
    class Meta():
        model = Ticket
        fields = ['title', 'description']

class editTicket(forms.Form):
    description = forms.CharField(max_length=100)
    status = forms.CharField(label="Status",
    widget=forms.Select(choices=status_choices))
    priority = forms.CharField(max_length=15, widget=forms.Select(choices=priority_choices))
    type = forms.CharField(max_length=15, widget=forms.Select(choices=type_choices))
