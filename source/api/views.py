from rest_framework import viewsets
from webapp.models import Task, Project
from .serializers import TasksSerializer, ProjectsSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    queryset =Task.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    queryset = Project.objects.all()

