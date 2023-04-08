from django.urls import path
from . import views

urlpatterns = [
    path("", views.posts_view, name="my_posts"),
    path("create", views.create_post, name="create_post"),
    path("delete/<int:id>", views.delete_post, name="delete_post"),
    path("edit", views.edit_post, name="edit_post"),
    path("<int:id>", views.post_detail, name="post_detail"),
    path("news", views.news, name="news")
]

# path("profile/<username>/edit/", views.edit_profile_view, name="edit"),
#     path("addfriend/<str:username>", views.add_friend, name="add_friend"),
#     path("removefriend/<str:username>", views.remove_friend, name="remove_friend"),
