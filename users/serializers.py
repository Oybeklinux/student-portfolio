from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'bio', 'location','profile_image', 'social_github','social_telegram','social_instagram', 'social_youtube', 'social_website', 'phone_number']