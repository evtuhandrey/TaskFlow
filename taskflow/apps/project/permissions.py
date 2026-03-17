from rest_framework import permissions


class IsOwnerOrCreator(permissions.BasePermission):
    """Разрешает удаление/изменение только владельцу воркспейса или создателю проекта."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.created_by == request.user or obj.workspace.woner == request.user
            