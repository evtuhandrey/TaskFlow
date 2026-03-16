from django.db import models
from django.conf import settings


class Workspace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null = True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_workspaces'
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='workspaces',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "workspaces"
        ordering = ['-created_at']

        
    def __str__(self):
        return self.name
