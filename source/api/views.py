from rest_framework import viewsets
from webapp.models import Project
from .serializers import ProjectsSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    queryset = Project.objects.all()


