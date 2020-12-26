from django import forms
from projects.models import Project

class projectForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ['name', 'description']

class editProject(forms.Form):
    description = forms.CharField(max_length=100)
