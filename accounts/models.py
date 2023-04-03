from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    phone = models.CharField(max_length=16, unique=True)
    blocked = models.BooleanField(default=False)
    bio = models.TextField(default="")
    updated_at = models.DateTimeField(default=timezone.now)
    business_account = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")
    is_request = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} friendship with: {self.friend}"


