from django import forms
from django.contrib.auth.models import User
from projects.models import Project
from core.models import User as core_user

role_options = [
    ('Admin', 'Admin'),
    ('Project Manager', 'Project Manager'),
    ('Developer', 'Developer'),
    ('None', 'None')
]

class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class joinForm(forms.ModelForm):
    role = forms.CharField(max_length=15, widget=forms.Select(choices=role_options))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        help_texts = {
            'username': None
        }

class editRoles(forms.Form):
    username = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'))
    role = forms.CharField(max_length=15, widget=forms.Select(choices=role_options))

class editProject(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all().order_by('name'))
    project_manager = forms.ModelChoiceField(queryset=core_user.objects.filter(role='Project Manager'))
    project_developer = forms.ModelChoiceField(queryset=core_user.objects.filter(role='Developer'))
