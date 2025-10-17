from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer
from projects.models import Project

class ProjectTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_project(self):
        project = Project.objects.get(pk=self.kwargs['project_id'])
        if project.user != self.request.user:
            raise PermissionDenied("You do not have access to this project")
        return project

    def get_queryset(self):
        project = self.get_project()
        return project.tasks.all().order_by('-created_at')

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(project=project)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__user=self.request.user)
