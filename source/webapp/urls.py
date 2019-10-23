from django.urls import path
from .views import IndexView, TaskView, TaskCreateView, TaskUpdateView, TaskDeleteView,\
    StatusIndexView,TypeIndexView, StatusCreateView, TypeCreateView, StatusUpdateView, TypeUpdateView, \
    StatusDeleteView, TypeDeleteView, ProjectIndexView, ProjectView, TaskProjectCreateView,\
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView

app_name = 'webapp'

urlpatterns = [
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
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete')
]