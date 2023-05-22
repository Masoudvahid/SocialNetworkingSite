from rest_framework import serializers
from .models import Messages
from accounts.models import User
from cryptography.fernet import Fernet


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SlugRelatedField(
        many=False, slug_field="username", queryset=User.objects.all()
    )
    receiver_name = serializers.SlugRelatedField(
        many=False, slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Messages
        fields = ["sender_name", "receiver_name", "message", "time"]
