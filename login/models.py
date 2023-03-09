from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=16, unique=True)
    blocked = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    bio = models.TextField(default="")

    # created_at = models.DateTimeField(default=timezone.now
    # Not necessary, since it is already in AbstractUser

    updated_at = models.DateTimeField(default=timezone.now)
    business_account = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "phone"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
