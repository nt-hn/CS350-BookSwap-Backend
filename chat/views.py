from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import CreateChat, Chat
from .serializers import CreateChatSerializer, ChatSerializer
# Create your views here.

@api_view(['POST'])
def create_chat(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            mutable_data = request.data.copy()
            mutable_data['chat_member_1'] = request.user.id
            serializer = CreateChatSerializer(data=mutable_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_chats(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            chats = CreateChat.objects.filter(chat_member_1=request.user) | CreateChat.objects.filter(chat_member_2=request.user)
            serializer = CreateChatSerializer(chats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_chat(request, chat_id):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            chats = CreateChat.objects.get(id=chat_id)
            chats.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_messeges(request, chat_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            chats = Chat.objects.filter(chatroom = chat_id).order_by('time')
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_messages(request, chat_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            chatroom = CreateChat.objects.get(id = chat_id)
            if chatroom.chat_member_1 == request.user or chatroom.chat_member_2 == request.user:
                message = Chat(chatroom=chatroom, user=request.user, text=request.POST.get('message'))
                message.save()
                chats = Chat.objects.filter(chatroom = chat_id)
                serializer = ChatSerializer(chats, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)