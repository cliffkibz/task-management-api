from rest_framework import viewsets, generics, permissions
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Project.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save()


class ProjectTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        return Task.objects.filter(
            project__id=project_id, project__user=self.request.user
        )

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_id")
        
        project = get_object_or_404(Project, id=project_id)
        
        if project.user != self.request.user:
            raise PermissionDenied("You do not have permission to add tasks to this project.")
        serializer.save(project=project)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def get_object(self):
        project_id = self.kwargs.get("project_id")
        pk = self.kwargs.get("pk")
        project = get_object_or_404(Project, id=project_id)
        if project.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Not allowed to access tasks for this project.")
        return get_object_or_404(Task, id=pk, project=project)
