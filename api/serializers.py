from rest_framework import serializers
from django.contrib.auth.models import User

from projects.models import Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    class Meta:
        model = Project
        fields = '__all__'