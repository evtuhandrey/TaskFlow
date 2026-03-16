from rest_framework import serializers
from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.email')
    members_count = serializers.IntegerField(source = 'members.count', read_only = True)


    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'owner', 'members_count', 'created_at']
        read_only_fields = ['created_at', 'owner']


class WorkspaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['name', 'description']

    
    def create(self, validated_data):
        user = self.context['request'].user
        workspace = Workspace.objects.create(owner = user, **validated_data)
        workspace.members.add(user)
        return workspace


