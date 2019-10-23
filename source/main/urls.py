"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from webapp.views import IndexView, TaskView, TaskCreateView, TaskUpdateView, TaskDeleteView,\
    StatusIndexView,TypeIndexView, StatusCreateView, TypeCreateView, StatusUpdateView, TypeUpdateView, \
    StatusDeleteView, TypeDeleteView, ProjectIndexView, ProjectView, TaskProjectCreateView,\
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView
from accounts.views import login_view, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('task/add/', TaskCreateView.as_view(), name='task_add'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('statuses/', StatusIndexView.as_view(), name='status_index'),
    path('types/', TypeIndexView.as_view(), name='type_index'),
    path('statuses/add/', StatusCreateView.as_view(), name='status_add'),
    path('types/add/', TypeCreateView.as_view(), name='type_add'),
    path('statuses/<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('types/<int:pk>/update/', TypeUpdateView.as_view(), name='type_update'),
    path('statuses/<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
    path('types/<int:pk>/delete/', TypeDeleteView.as_view(), name='type_delete'),
    path('projects/', ProjectIndexView.as_view(), name='project_index'),
    path('projects/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('projects/<int:pk>/task_add/', TaskProjectCreateView.as_view(), name='project_task_create'),
    path('projects/add', ProjectCreateView.as_view(), name='project_add'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout')

]
