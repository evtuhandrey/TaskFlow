from rest_framework import serializers, generics
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(write_only=True, validators = [validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    
    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password" : "Пароли не совпадают."}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user
    

class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request = self.context.get('request'),
                username = email,
                password = password
            )

            if not user:
                raise serializers.ValidationError(
                    'Пользователь не найден.'
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    'Аккаунт пользователя отключен.'
                )
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                    'Должен включать в себя "email" и "password".'
                )


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя"""
    full_name = serializers.ReadOnlyField()
    tasks_count = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    active_tasks = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = (
            "id", 
            "email",
            "username",
            "full_name",
            "avatar",
            "bio",
            "created_at",
            "tasks_count",
            "completed_tasks",
            "active_tasks",
        )

    def get_tasks_count(self, obj):
        return obj.assigned_tasks.count()
    
    def get_completed_tasks(self, obj):
        return obj.assigned_tasks.filter(status = "done").count()
    
    def get_active_tasks(self, obj):
        return obj.assigned_tasks.exclude(stauts = "done").count()
    

class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля пользователя"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'bio')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        
            