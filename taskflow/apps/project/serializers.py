from rest_framework import serializers
from .models import Project, Workspace


class ProjectSerializer(serializers.ModelSerializer):
    workspace_name = serializers.ReadOnlyField(source = 'workspace.name')
    created_by_email = serializers.ReadOnlyField(source = 'created_by.email')
    

    class Meta:
        model = Project
        fields = ['id', 'workspace', 'workspace_name', 'title', 'description', 'created_by_email', 'created_at']
        read_only_fields = ['created_at', 'workspace']

class ProjectCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = Project
        fields = ['id', 'workspace', 'title', 'description']

    def create(self, validated_data):
        request = self.context['request']
        workspace_id = self.context['view'].kwargs.get('workspace_id')

        workspace = Workspace.objects.get(id=workspace_id)

        return Project.objects.create(
            workspace = workspace,
            created_by = request.user,
            **validated_data
        )

    
    def validate_workspace(self, value):
        user = self.context['request'].user
        if value.owner != user and user not in value.members.all():
            raise serializers.ValidationError("Вы не являетесь участником этого воркспейса!")
        return value
    

class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description']
        