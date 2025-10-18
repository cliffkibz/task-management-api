from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User
# from tasks.serializers import TaskSerializer

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'status', 'due_date', 'priority']
        read_only_fields = ['id', 'project']

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'description', 'created_at', 'tasks']
        read_only_fields = ['id']