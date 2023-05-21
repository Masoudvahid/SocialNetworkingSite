from django.urls import path
from . import views

urlpatterns = [
    path("", views.posts_view, name="my_posts"),
    path("create", views.create_post, name="create_post"),
    path("delete/<int:id_post>", views.delete_post, name="delete_post"),
    path("news", views.news, name="news"),
    path("like/<int:id_post>", views.like_post, name="like_post"),
    path("news/popup/<int:id_post>", views.pop_up, name="pop_up"),
]

# path("profile/<username>/edit/", views.edit_profile_view, name="edit"),
#     path("addfriend/<str:username>", views.add_friend, name="add_friend"),
#     path("removefriend/<str:username>", views.remove_friend, name="remove_friend"),
