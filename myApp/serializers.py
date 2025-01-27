from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
#write a serializer for the Blog model
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id','image', 'title', 'description', 'author', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        blog = Blog.objects.create(**validated_data)
        return blog