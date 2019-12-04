from rest_framework import viewsets
from webapp.models import Task
from .serializers import TasksSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    queryset =Task.objects.all()


