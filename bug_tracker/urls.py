"""bug_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from projects import views as project_views
from tickets import views as ticket_views
from rest_framework import routers
#for file storage
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'projects', project_views.ProjectViewSet)
router.register(r'users', project_views.UserViewSet)
router.register(r'tickets', ticket_views.TicketViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_profile/', core_views.user_profile, name="user_profile"),
    path('', core_views.user_login, name="login"),
    path('join/', core_views.user_join, name="join"),
    path('logout/', core_views.user_logout, name="logout"),
    path('core/', core_views.core_home, name="home"),
    path('projects/', project_views.project_home, name="projects"),
    path('add_project/', project_views.add_project, name="add_project"),
    path('projects/details/<str:name>/', project_views.details_project, name="details_project"),
    path('projects/edit/<str:name>/', project_views.edit_project, name="edit_project"),
    path('projects/delete/<str:name>/', project_views.delete_project, name="delete_project"),
    path('tickets/', ticket_views.ticket_home, name="tickets"),
    path('add_ticket/', ticket_views.add_ticket, name="add_ticket"),
    path('tickets/details/<str:name>/', ticket_views.details_ticket, name="ticket_details"),
    path('tickets/edit/<str:name>/', ticket_views.edit_ticket, name="edit_ticket"),
    path('tickets/delete/<str:name>/', ticket_views.delete_ticket, name="delete_ticket"),
    path('tickets_sort_priority/', ticket_views.sort_priority, name="tickets_sort_priority"),
    path('tickets_sort_date/', ticket_views.sort_date, name="tickets_sort_date"),
    path('manage_roles/', core_views.manage_roles, name='manage_roles'),
    path('manage_projects/', core_views.manage_projects, name='manage_projects'),
    #rest stuff
    path('api/v1/', include(router.urls)),
    path('api-auth/v1/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
