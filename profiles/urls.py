from django.urls import path
from . import views

urlpatterns = [
    path("profile/<username>/", views.profile_view, name="view"),
    path("profile/<username>/edit/", views.edit_profile_view, name="edit"),
    path("addfriend/<str:username>", views.add_friend, name="add_friend"),
]
