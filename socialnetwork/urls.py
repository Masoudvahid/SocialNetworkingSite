"""socialnetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainpage import views as mainpage_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("login.urls")),
    path("home/", include("mainpage.urls")),
    path("", mainpage_views.home_view, name="empty_address"),
    path("", include("search.urls")),
    path("", include(("profiles.urls", "profile"), namespace="profile")),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='profiles/password_change_done.html'),
         name="password_change_done"),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='profiles/password_change.html'),
         name="password_change"),
]
