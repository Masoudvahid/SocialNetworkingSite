from .models import Post
from accounts.models import User
from rest_framework import serializers
from datetime import datetime


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Post
        fields = ["author", "updated_on", "content", "created_on", "likes"]
