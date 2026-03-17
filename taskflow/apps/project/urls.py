from django.urls import path
from . import views

urlpatterns = [
    path('workspaces/<int:workspace_id>/projects/', views.ProjectCreateView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
]