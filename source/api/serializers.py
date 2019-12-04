from rest_framework import serializers
from webapp.models import Task, Project


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields = ('id', 'summary', 'description', 'status', 'type', 'created_at', 'updated_at', 'project', 'created_by', 'assigned_to')



class ProjectsSerializer(serializers.ModelSerializer):
    tasks= TasksSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description','created_at', 'updated_at', 'tasks')