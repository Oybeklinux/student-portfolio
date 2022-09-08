from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from users.manager import UserManager

class User(AbstractUser):
    ROLE = [
        ('admin', 'admin'),
        ('developer', 'developer'),
        ('guest', 'guest'),
        ('empoloyee', 'empoloyee')
    ]
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='portfolio', blank=True, null=True)
    social_github = models.CharField(max_length=100, blank=True, null=True)
    social_telegram = models.CharField(max_length=100, blank=True, null=True)
    social_instagram = models.CharField(max_length=100, default="instagram")
    social_youtube = models.CharField(max_length=100, blank=True, null=True)
    social_website = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    phone_regex = RegexValidator(
        regex=r'^998\d{9}$', message="Telefon raqam 9981234567 formatida bo'lishi kerak")
    phone_number = models.CharField(
        max_length=12, unique=True, validators=[phone_regex])
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, default="")
    count = models.IntegerField(default=0)
    role = models.CharField(max_length=10, choices=ROLE, default='developer')
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()
