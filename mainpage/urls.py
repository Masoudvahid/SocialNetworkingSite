from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("news", views.news, name="news"),
    path("friends_bar/", views.friends_bar, name="friends_bar"),
]
