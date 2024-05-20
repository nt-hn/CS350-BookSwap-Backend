from rest_framework import serializers
from .models import CreateChat, Chat
from account_api.serializers import UserSerializer

class CreateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateChat
        fields = ['chat_member_1', 'chat_member_2']

class ChatSerializer(serializers.ModelSerializer):
    user = UserSerializer()  

    class Meta:
        model = Chat
        fields = ['chatroom', 'user', 'time', 'text']
