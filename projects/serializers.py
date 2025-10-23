from rest_framework import serializers
from .models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "due_date",
            "priority",
            "created_at",
        ]
        read_only_fields = ["id", "project", "created_at"]


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "user", "title", "description", "created_at", "tasks"]
        read_only_fields = ["id", "user", "created_at"]
