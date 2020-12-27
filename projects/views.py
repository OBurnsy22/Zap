from django.shortcuts import render, redirect
from projects.forms import projectForm, editProject
from projects.models import Project
from django.contrib.auth.decorators import login_required
from tickets.views import retrieve_tickets
from core.models import User
from tickets.models import Ticket
#rest stuff
from rest_framework import viewsets
from rest_framework import permissions
from projects.serializers import ProjectSerializer, UserSerializer
from django.contrib.auth.models import User as django_user


# Create your views here.
@login_required(login_url='/')
def project_home(request):
    page_data={"rows":[], "add_project":projectForm}
    populate_page_data(request, page_data)
    return render(request, 'projects/project_home.html', context=page_data)

def add_project(request):
    #this is an admin and project manager only page, check role of user first
    user_obj = User.objects.get(pk=request.user.username)
    if(user_obj.role != "Admin"):
        return redirect('/core/')
    page_data={"rows":[], "add_project":projectForm}
    if request.method == "POST" and "Add Project" in request.POST:
        project_form = projectForm(request.POST)
        if(project_form.is_valid()):
            Project(name=project_form.cleaned_data['name'],
                description=project_form.cleaned_data['description']).save()
            return redirect("/projects/")
    return render(request, 'projects/add_project.html', context=page_data)

def details_project(request, name):
    #rows contains project object data
    page_data={"rows":[], "tickets":[], "project_name":" ", "project_description":" "}
    project_obj = Project.objects.get(pk=name)
    #get tickets relating to project
    retrieve_tickets(request, project_obj, page_data)
    #get info of project_obj
    row=[]
    page_data["project_name"] = project_obj.name
    page_data["project_description"] = project_obj.description
    populate_page_data_with_project_users(request, page_data, project_obj)
    return render(request, 'projects/project_details.html', context=page_data)

def edit_project(request, name):
    #this is an admin and project manager only page, check role of user first
    user_obj = User.objects.get(pk=request.user.username)
    if(user_obj.role != "Admin" and user_obj.role != "Project Manager"):
        return redirect('/core/')
    page_data={"rows":[], "edit_project": editProject}
    if request.method == "POST" and "Edit Project" in request.POST:
        project_form = editProject(request.POST)
        if project_form.is_valid():
            project_obj = Project.objects.get(pk=name)
            project_obj.description = project_form.cleaned_data['description']
            project_obj.save()
            return redirect('/projects/')
    #prepopulate fields before going to edit page
    project_obj = Project.objects.get(pk=name)
    project_form = editProject(initial={'description':project_obj.description})
    page_data["edit_project"] = project_form
    return render(request, 'projects/project_edit.html', context=page_data)

def delete_project(request, name):
    project_object = Project.objects.get(pk=name)
    #remove all tickets corresponding to this project
    ticket_objects = Ticket.objects.all()
    for ticket in ticket_objects:
        if ticket.project == project_object:
            ticket.delete()
    #remove this project object from whatever users it may be assigned to
    user_objects = User.objects.all()
    for user in user_objects:
        if user.project == project_object:
            user.project = None
    #delete project
    project_object.delete()
    page_data={"rows":[]}
    populate_page_data(request, page_data)
    return render(request, 'projects/project_home.html', context=page_data)

def populate_page_data(request, page_data):
    project_objects = Project.objects.all()
    for projects in project_objects:
        row=[]
        row.append(projects.name)
        row.append(projects.description)
        page_data.get("rows").append(row)
    return

def populate_page_data_with_project_users(request, page_data, project_obj):
    user_objects = User.objects.all()
    for user in user_objects:
        if user.project == project_obj:
            row=[]
            row.append(user.username)
            row.append(user.email)
            row.append(user.role)
            page_data.get("rows").append(row)
    return

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tasks to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = django_user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
