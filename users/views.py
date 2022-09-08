from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .helpers import send_otp_to_phone
from .models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework import filters

from .serializers import UserSerializer


@api_view(["GET"])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')


@api_view(['POST'])
def login_user(request):
    data = request.data
    phone = request.data.get('phone_number')
    sms = data.get('sms')

    if phone is None:
        return Response({
            'status': 400,
            'message': 'Telefon raqam talab etiladi'
        })

    if not phone.isdigit() or len(phone) != 12:
        return Response({
            'status': 400,
            'message': "Telefon raqam 998971234567 formatida bo'lishi kerak"
        })
    try:
        user = User.objects.get(phone_number=phone)
    except Exception as e:
        return Response({
            'status': 400,
            'message': "Bunday raqam bazada yo'q. Qayta ro'yxatdan o'ting"
        })

    try:
        token = Token.objects.get_or_create(user=user)[0].key

    except Exception as e:
        print(e)

    if sms is None:
        return Response({
            'status': 400,
            'message': 'sms talab etiladi'
        })

    if len(sms) != 6:
        return Response({
            'status': 400,
            "message": "sms 6 raqamdan iborat bo'lishi kerak"
        })

    user = None
    try:
        user = User.objects.get(phone_number=phone, otp=sms)
        user.is_phone_verified = True
        user.save()
    except Exception as e:
        return Response({
            'status': 400,
            'message': 'Raqam yoki sms kod xato'
        })

    # token = Token.objects.create(user=user)
    if user.is_active:
        login(request, user)
        return Response({
            'status': 200,
            'user_id': user.id,
            'token': token,
            "is_admin": user.is_staff,
            "phone": phone,
            "user_name": user.first_name,
        })
    else:
        raise Response({
            'status': 400,
            'message': 'Foydalnuvchi faollashtirilmagan'
        })


@api_view(['POST'])
def register_user(request):
    data = request.data
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    username = request.data.get('username')
    phone = request.data.get('phone_number')
    if request.data.get('password', None) is not None:
        password = request.data.get('password')
    else:
        password = phone

    if first_name is None:
        return Response({
            'status': 400,
            'message': 'Ism talab etiladi'
    })

    if last_name is None:
        return Response({
            'status': 400,
            'message': 'Familiya talab etiladi'
    })

    if phone is None:
        return Response({
            'status': 400,
            'message': 'Telefon raqam talab etiladi'
    })

    if username is None:
        return Response({
            'status': 400,
            'message': 'login talab etiladi'
    })

    if not phone.isdigit() or len(phone) != 12:
        return Response({
            'status': 400,
            'message': "Telefon raqam 998971234567 formatida bo'lishi kerak"
        })
    user = None
    try:
        user = User.objects.get(phone_number=phone)
        return Response({
            'status': 400,
            'message': 'Bu foydalanuvchi bor'
        })
    except Exception as e:
        pass

    try:
        sms, error = send_otp_to_phone(phone)
        if error:
            return Response({
                'status': 400,
                'message': 'SMS yuborishda xatolik. Qayta yuboring',
                'detail': str(error)
            })
        user = User.objects.create(
            phone_number=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            otp=sms
        )
        # make_password()


    except Exception as e:
        return Response({
            'status': 400,
            'message': 'Foydalanuvchi yaratishda xatolik yuz berdi',
            "detail": str(e)
        })

    return Response({
        'status': 200,
        'message': 'SMS yuborildi',
        'user_id': user.id,
        'otp': sms if settings.DEBUG else None,
        "is_admin": user.is_staff,
        "phone": phone,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "username": username
    })


@api_view(['POST'])
def send_sms_to_login(request):
    data = request.data
    phone = request.data.get('phone_number')

    if phone is None:
        return Response({
            'status': 400,
            'message': 'Telefon raqam talab etiladi'
        })

    if not phone.isdigit() or len(phone) != 12:
        return Response({
            'status': 400,
            'message': "Telefon raqam 998971234567 formatida bo'lishi kerak"
        })
    user = None
    try:
        user = User.objects.get(phone_number=phone)
    except Exception as e:
        return Response({
            'status': 400,
            'message': "Bunday foydalanuvchi mavjud emas. Ro'yxatdan o'ting"
        })

    sms, error = send_otp_to_phone(phone)
    if not sms:
        return Response({
            'status': 400,
            'message': 'SMS yuborishda xatolik. Qayta yuboring',
            'error': error

        })
    user.otp = sms
    user.save()
    return Response({
        'status': 200,
        'message': 'SMS yuborildi',
        'user_id': user.id,
        'otp': sms if settings.DEBUG else None
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='developer')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'username']
    http_method_names = ['get', 'patch', 'put', 'delete']