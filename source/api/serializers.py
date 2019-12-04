from rest_framework import serializers
from webapp.models import Task


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields = ('id', 'summary', 'description', 'status', 'type', 'created_at', 'updated_at', 'project', 'created_by', 'assigned_to')