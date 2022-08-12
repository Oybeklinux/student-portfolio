from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .models import Profile
from .serializers import UsersSerializer


class UserView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UsersSerializer
