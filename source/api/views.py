from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Task, Project
from .serializers import TasksSerializer, ProjectsSerializer


class LogoutView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    queryset =Task.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    queryset = Project.objects.all()

