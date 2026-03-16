from django.urls import path, include
from . import views


urlpatterns = [
    path('workspaces/', views.WorkspaceView.as_view(), name = 'workspace_list'),
    path('workspaces/<int:pk>', views.WorkspaceDetailView.as_view(), name = 'workspace_detail'),
]