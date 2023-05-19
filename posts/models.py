from django.db import models
from accounts.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='author')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    class Meta:
        ordering = ['-created_on']
