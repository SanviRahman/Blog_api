from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog, Comment


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
        fields = ('id','image', 'title', 'description', 'author', 'comment','created_at', 'updated_at',)
    
    def create(self, validated_data):
        blog = Blog.objects.create(**validated_data)
        return blog
    

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)  # Include email

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'email', 'comment', 'blog')


    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
