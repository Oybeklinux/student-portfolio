from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_user),
    path('logout/', logout_user),
    path('register/', register_user),
    path('send_sms/', send_sms_to_login)
]

