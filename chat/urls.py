from django.urls import path
from . import views

urlpatterns = [
    path("create_chat/", views.create_chat, name="create_chat"),
    path("get_chats/", views.get_chats, name="get_chats"),
    path("get_messeges/<int:chat_id>/", views.get_messeges, name="get_messeges"),
    path("create_messages/<int:chat_id>/", views.create_messages, name="create_messages"),
]