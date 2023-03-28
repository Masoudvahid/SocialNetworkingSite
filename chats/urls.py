from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.chats, name="chats"),
    #path("search/", views.search, name="search_chats"),
    path("<str:username>", views.chat, name="chat"),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
]
