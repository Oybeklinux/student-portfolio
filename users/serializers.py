from rest_framework import serializers
from projects.serializers import ProjectSerializer
from .models import Profile


class UsersSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = '__all__'