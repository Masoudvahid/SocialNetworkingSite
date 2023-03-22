from django.contrib import admin

from .models import User, Friends

admin.site.register(Friends)
admin.site.register(User)
