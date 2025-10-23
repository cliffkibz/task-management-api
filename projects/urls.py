from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    TaskViewSet,
    ProjectTaskListCreateView,
    TaskDetailView,
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "projects/<int:project_id>/tasks/",
        ProjectTaskListCreateView.as_view(),
        name="project-tasks",
    ),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
