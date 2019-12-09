from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Task, Project
from .serializers import TasksSerializer, ProjectsSerializer, UserSerializer


class LogoutView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'response': user})
        return Response(serializer.errors)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = TasksSerializer
    queryset = Task.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = ProjectsSerializer
    queryset = Project.objects.all()

