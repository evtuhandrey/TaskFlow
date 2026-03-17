from rest_framework import generics, permissions
from .models import Project
from django.db.models import Q
from rest_framework.response import Response
from .serializers import(
    ProjectSerializer, 
    ProjectCreateSerializer,
    ProjectUpdateSerializer
    )


class ProjectCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(created_by = user) | Q(workspace__owner = user) | Q(workspace__members=user)
        ).distinct().select_related("workspace", "created_by")
    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateSerializer
        return ProjectSerializer
    


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(created_by = user) | Q(workspace__owner = user) | Q(workspace__members=user)
        ).distinct()
    
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectUpdateSerializer
        return ProjectSerializer


