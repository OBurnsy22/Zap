from django.shortcuts import render, redirect
from tickets.models import Ticket, ticketHistory, File
from tickets.forms import ticketForm, editTicket, fileUpload
from django.contrib.auth.decorators import login_required
from projects.models import Project
from core.models import User
from operator import itemgetter
import enum
#files
from django.core.files.storage import FileSystemStorage
#rest stuff
from rest_framework import viewsets
from rest_framework import permissions
from tickets.serializers import TicketSerializer, UserSerializer
from django.contrib.auth.models import User as django_user
# Create your views here.

@login_required(login_url='/')
def ticket_home(request):
    page_data={"rows":[], "add_ticket":ticketForm}
    populate_page_data(request, page_data)
    return render(request, 'tickets/ticket_home.html', context=page_data)

def add_ticket(request):
    #this is an admin and project manager only page, check role of user first
    user_obj = User.objects.get(pk=request.user.username)
    if(user_obj.role != "Admin" and user_obj.role != "Project Manager"):
        return redirect('/core/')
    page_data={"rows":[], "add_ticket":ticketForm}
    if request.method == "POST" and "Add Ticket" in request.POST:
        ticket_form = ticketForm(request.POST)
        if(ticket_form.is_valid()):
            Ticket(title=ticket_form.cleaned_data['title'],
                description=ticket_form.cleaned_data['description'],
                project=ticket_form.cleaned_data['project'],
                priority=ticket_form.cleaned_data['priority'],
                type=ticket_form.cleaned_data['type']).save()
            return redirect('/tickets/')
    return render(request, 'tickets/add_ticket.html', context=page_data)

def details_ticket(request, name):
    breakpoint()
    page_data={"rows":[], "ticket_name":" ", "file_upload":fileUpload}
    ticket_obj = Ticket.objects.get(pk=name)
    #user is uploading ifle
    if request.method == "POST" and "Add File" in request.POST:
        uploadForm = fileUpload(request.POST, request.FILES)
        if(uploadForm.is_valid()):
            #get the file
            uploaded_file = request.FILES['file']
            #save the file
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            #create File objects
            File(title=uploadForm.cleaned_data['title'],
            file=uploaded_file,
            ticket = ticket_obj).save()
        else:
            print(uploadForm.errors)
    row=[]
    row.append(ticket_obj.description)
    row.append(ticket_obj.project.name)
    row.append(ticket_obj.priority)
    row.append(ticket_obj.status)
    row.append(ticket_obj.type)
    row.append(ticket_obj.date)
    page_data.get("rows").append(row)
    page_data["ticket_name"]=ticket_obj.title
    return render(request, 'tickets/ticket_details.html', context=page_data)

def populate_page_data(request, page_data):
    ticket_objects = Ticket.objects.all()
    for tickets in ticket_objects:
        row=[]
        row.append(tickets.title)
        row.append(tickets.description)
        row.append(tickets.status)
        row.append(tickets.project)
        row.append(tickets.priority)
        row.append(tickets.type)
        row.append(tickets.date)
        page_data.get("rows").append(row)
    return

def edit_ticket(request, name):
    #this is an admin and project manager only page, check role of user first
    user_obj = User.objects.get(pk=request.user.username)
    if(user_obj.role != "Admin" and user_obj.role != "Project Manager" and user.obj.role != "Developer"):
        return redirect('/core/')
    page_data={"rows":[], "edit_ticket": editTicket}
    if request.method == "POST" and "Edit Ticket" in request.POST:
        ticket_form = editTicket(request.POST)
        if ticket_form.is_valid():
            ticket_obj = Ticket.objects.get(pk=name)
            #create a new ticket history object with every newly changed field
            #if ticket_obj.description != ticket_form.cleaned_data['description']:
                #ticketHistory(old_value=ticket_obj.description,
                #new_value=ticket_form.cleaned_data['description'],
                #project=ticket_obj.project, changed_property='Description').save()
            ticket_obj.description = ticket_form.cleaned_data['description']
            #if ticket_obj.status != ticket_form.cleaned_data['status']:
                #ticketHistory(old_value=ticket_obj.status,
                #new_value=ticket_form.cleaned_data['status'],
                #project=ticket_obj.project, changed_property='Status').save()
            ticket_obj.status = ticket_form.cleaned_data['status']
            #if ticket_obj.priority != ticket_form.cleaned_data['priority']:
                #ticketHistory(old_value=ticket_obj.priority,
                #new_value=ticket_form.cleaned_data['priority'],
                #project=ticket_obj.project, changed_property='Priority').save()
            ticket_obj.priority = ticket_form.cleaned_data['priority']
            #if ticket_obj.type != ticket_form.cleaned_data['type']:
                #ticketHistory(old_value=ticket_obj.type,
                #new_value=ticket_form.cleaned_data['type'],
                #project=ticket_obj.project, changed_property='Type').save()
            ticket_obj.type = ticket_form.cleaned_data['type']
            ticket_obj.save()
            #creat a ticket history object for history table
            return redirect('/tickets/')
    #prepopulate fields before going to edit page
    ticket_obj = Ticket.objects.get(pk=name)
    ticket_form = editTicket(initial={'description':ticket_obj.description,
    'priority':ticket_obj.priority,
    'type':ticket_obj.type})
    page_data["edit_ticket"] = ticket_form
    return render(request, 'tickets/ticket_edit.html', context=page_data)

def delete_ticket(request, name):
    ticket_object = Ticket.objects.get(pk=name)
    ticket_object.delete()
    return redirect("/tickets/")

def retrieve_tickets(request, project_obj, page_data):
    tickets = Ticket.objects.all()
    for objects in tickets:
        if objects.project == project_obj:
            row=[]
            row.append(objects.title)
            row.append(objects.description)
            row.append(objects.status)
            row.append(objects.project)
            row.append(objects.priority)
            row.append(objects.type)
            row.append(objects.date)
            page_data.get("tickets").append(row)
    return

def populate_page_data_by_priority(request, page_data):
    class priority(enum.Enum):
        High = 3
        Medium = 2
        Low = 1
        none = 0
    ticket_objects = Ticket.objects.all()
    for prio in priority:
        for tickets in ticket_objects:
            if tickets.priority == prio.name or (prio.name == "none" and tickets.priority == "None"):
                row=[]
                row.append(tickets.title)
                row.append(tickets.description)
                row.append(tickets.status)
                row.append(tickets.project)
                row.append(tickets.priority)
                row.append(tickets.type)
                row.append(tickets.date)
                page_data.get("rows").append(row)
    return

def sort_priority(request):
    page_data={"rows":[], "add_ticket":ticketForm}
    populate_page_data_by_priority(request, page_data)
    return render(request, 'tickets/ticket_home.html', context=page_data)

def sort_date(request):
    page_data={"rows":[], "add_ticket":ticketForm}
    populate_page_data(request, page_data)
    rows_of_tickets=page_data.get("rows")
    page_data["rows"]=sorted(rows_of_tickets, key=itemgetter(6))
    return render(request, 'tickets/ticket_home.html', context=page_data)

def retrieve_ticket_data(page_data):
    tickets = Ticket.objects.all()
    feature, bug, comment = 0, 0, 0
    none, low, medium, high = 0, 0, 0, 0
    open, in_progress, closed, resolved = 0, 0, 0, 0
    for objects in tickets:
        #record ticket type
        if(objects.type == "Feature Request"):
            feature+=1
        elif(objects.type == "Bug/Error"):
            bug+=1
        else:
            comment+=1
        #record ticket priority
        if(objects.priority == "None"):
            none+=1
        elif(objects.priority == "Low"):
            low+=1
        elif(objects.priority == "Medium"):
            medium+=1
        else:
            high+=1
        #record ticket status
        if(objects.status == "Open"):
            open+=1
        elif(objects.status== "In Progress"):
            in_progress+=1
        elif(objects.status == "Closed"):
            closed+=1
        else:
            resolved+=1
    page_data["ticket_feature_count"] = feature
    page_data["ticket_bug_count"] = bug
    page_data["ticket_comment_count"] = comment
    page_data["ticket_low"] = low
    page_data["ticket_medium"] = medium
    page_data["ticket_high"] = high
    page_data["ticket_none"] = none
    page_data["ticket_open"] = open
    page_data["ticket_in_progress"] = in_progress
    page_data["ticket_closed"] = closed
    page_data["ticket_resolved"] = resolved
    page_data["ticket_type_total"] = feature + bug + comment

class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tasks to be viewed or edited.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
