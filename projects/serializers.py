from rest_framework import serializers
from .models import *
from users.serializers import UserSerializer
import re


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    tag = TagSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'


    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

    # def validate_name(self, value):
    #     if re.search('\d', value):
    #         raise serializers.ValidationError('Malaka nomida son kelmasin')
    #
    #     return value.lower()

    def validate(self, data):
        if re.search('\d', data['name']):
            raise serializers.ValidationError('Malaka nomida son kelmasin')
        if 1 < len(data['description']) < 10:
            raise serializers.ValidationError('Tavsif 10 harfdan kam bo''lmasin')
        data['name'] = data['name'].lower()
        return data

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
