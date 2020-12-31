from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from core.forms import loginForm as login_form
from core.forms import joinForm as join_form
from core.forms import editRoles as edit_roles
from core.forms import editProject as edit_project
from core.models import User
from projects.models import Project
from tickets.views import retrieve_ticket_data

# Create your views here.
@login_required(login_url='/')
def core_home(request):
    page_data={"ticket_feature_count":0, "ticket_bug_count":0, "ticket_comment_count":0,
    "ticket_low":0, "ticket_medium":0, "ticket_high":0, "ticket_none":0,
    "ticket_open":0, "ticket_in_progress":0, "ticket_closed":0, "ticket_resolved":0,
    "ticket_type_total":0, "ticket_types":[], "ticket_count":[]}
    retrieve_ticket_data(page_data)
    return render(request, 'core/core_home.html', context=page_data)

#bar chart: return list of labels and list of values

def user_login(request):
    if (request.method == 'POST'):
        form = login_form(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"],
            password=form.cleaned_data["password"])
            #if user is authenticated
            if user:
                #check if account is active
                if user.is_active:
                    #log in user
                    login(request, user)
                    return redirect("/core/")
                else:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(form.cleaned_data["username"],
                form.cleaned_data["password"]))
                return render(request, 'core/login.html', {"login_form": login_form})
    else:
        return render(request, 'core/login.html', {"login_form": login_form})

def user_join(request):
    if (request.method == "POST"):
        form = join_form(request.POST)
        if form.is_valid():
            #save for to DB
            user = form.save()
            #encrypt the password
            user.set_password(user.password)
            #save encrypted password to db
            user.save()
            #create Core User object
            User(username=form.cleaned_data.get("username"), password=form.cleaned_data.get("password"),
            role=form.cleaned_data.get("role"), firstName=form.cleaned_data.get("first_name"),
            lastName=form.cleaned_data.get("last_name"), email=form.cleaned_data.get("email")).save()
            #redirects back to login
            #login()
            return redirect('/')
        else:
            #form is invalid
            print("Join form validation failed.")
            return render(request, 'core/join.html', {"join_form": join_form})
    else:
        return render(request, 'core/join.html', {"join_form": join_form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def manage_roles(request):
    #this is an admin only page, check role of user first
    user_obj = User.objects.get(pk=request.user.username)
    if(user_obj.role != "Admin"):
        return redirect('/core/')
    page_data={"rows":[], "edit_roles":edit_roles}
    if request.method == "POST" and "Edit Roles" in request.POST:
        edit_form = edit_roles(request.POST)
        if(edit_form.is_valid()):
            user_obj = User.objects.get(pk=edit_form.cleaned_data['username'])
            user_obj.role = edit_form.cleaned_data['role']
            user_obj.save()
    populate_page_data_with_users(request, page_data)
    return render(request, 'core/manage_roles.html', context=page_data)

@login_required(login_url='/')
def manage_projects(request):
    #this is an admin only page, check role of user first
    user_obj = User.objects.get(pk=request.user.username)
    if(user_obj.role != "Admin"):
        return redirect('/core/')
    page_data={"rows":[], "edit_project":edit_project}
    if request.method == "POST" and "Edit Project" in request.POST:
        edit_form = edit_project(request.POST)
        if(edit_form.is_valid()):
            project_obj = Project.objects.get(pk=edit_form.cleaned_data['project'].name)
            manager_user_obj = User.objects.get(pk=edit_form.cleaned_data['project_manager'].username)
            developer_user_obj = User.objects.get(pk=edit_form.cleaned_data['project_developer'].username)
            #assign user objects project field
            manager_user_obj.project = project_obj
            manager_user_obj.save()
            developer_user_obj.project = project_obj
            developer_user_obj.save()
    populate_page_data_with_projects(request, page_data)
    return render(request, 'core/manage_projects.html', context=page_data)

def populate_page_data_with_projects(request, page_data):
    user_objects = User.objects.all()
    project_objects = Project.objects.all()
    for project in project_objects:
        row=[]
        row.append(project.name)
        #loop for project manager
        noUsers=True
        for user in user_objects:
            if user.role == "Project Manager" and user.project == project:
                row.append(user.username)
                noUsers=False
        #if there are no assigned project managers, append blank space
        if(noUsers == True):
            row.append("*No Assigned User*")
        #loop for project developers
        noUsers=True
        for user in user_objects:
            if user.role == "Developer" and user.project == project:
                row.append(user.username)
                noUsers=False
        #if there are no assigned project developers, append blank space
        if(noUsers == True):
            row.append("*No Assigned User*")
        page_data.get("rows").append(row)
    return

def populate_page_data_with_users(request, page_data):
    user_objects = User.objects.all()
    for users in user_objects:
        row=[]
        row.append(users.username)
        row.append(users.role)
        row.append(users.email)
        page_data.get("rows").append(row)
    return

def user_profile(request):
    page_data={"rows":[], "userName":""}
    User_obj = User.objects.get(pk=request.user.username)
    row=[]
    row.append(User_obj.firstName)
    row.append(User_obj.lastName)
    row.append(User_obj.username)
    row.append(User_obj.email)
    row.append(User_obj.project)
    row.append(User_obj.role)
    page_data.get("rows").append(row)
    page_data["userName"] = User_obj.username
    return render(request, 'core/user_profile.html', context=page_data)
