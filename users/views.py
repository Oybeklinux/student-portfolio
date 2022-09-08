from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile
from .serializers import *


class UserView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

from django.contrib.auth import authenticate, login, logout


@api_view(["GET"])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')


@api_view(['POST'])
def login_user(request):
    data = request.data
    print(data)
    login = data['username']
    password = data['password']

    if not login:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Login talab etiladi'
        })
    if not password:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Parol talab etiladi'
        })

    user = authenticate(username=login, password=password)
    print(user)
    if not user:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'bunday foydalanuvchi bazada yo''q'
        })

    token = Token.objects.get_or_create(user=user)[0].key
    return Response(
        {
            "token": token
        }
    )


@api_view(['POST'])
def register_user(request):
    data = request.data

    login = data['username']
    password = data['password']

    if not login:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Login talab etiladi'
        })
    if not password:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Parol talab etiladi'
        })

    user = authenticate(username=login, password=password)

    if user:
        return Response({
            'status': 400,
            'message': 'Bu foydalanuvchi bor'
        })


    try:
        user = User.objects.create(
            username=login,
            password=password
        )
    except Exception as e:
        return Response({
            'status': 400,
            'message': 'Foydalanuvchi yaratishda xatolik yuz berdi'
        })
    token = Token.objects.get_or_create(user=user)[0].key
    return Response({
        'message': 'Foydalanuvchi qo''shildi',
        "token": token,
        "is_admin": user.is_staff
    }, status=status.HTTP_201_CREATED)

