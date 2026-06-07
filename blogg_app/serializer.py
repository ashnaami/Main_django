from rest_framework import serializers
from .models import TB_User, TB_Post, TB_Comments

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TB_User
        fields='__all__'
        extra_kwargs = {
            "image": {"required": False}
        }

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TB_Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TB_Comments
        fields = ['id', 'user', 'post', 'comments'] 