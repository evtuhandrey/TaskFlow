from django.db import models
from django.conf import settings
from apps.workspaces.models import Workspace


class Project(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete = models.CASCADE,
        related_name='projects'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null = True,
        related_name='created_projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.workspace.name} | {self.title}"  
