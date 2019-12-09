from django.contrib.auth.models import User
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


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm')


        def create(self, **kwargs):
            username = User(username=self.validated_data['username'])
            password = self.validated_data['password']
            password_confirm = self.validated_data['password_confirm']
            if User.objects.get(username=username):
                raise serializers.ValidationError('User with this username already exists')
            if password != password_confirm:
                raise serializers.ValidationError({'password': 'Passwords do not match'})
            username.set_password(password)
            username.save()
            User.objects.create(username=username)
            return username