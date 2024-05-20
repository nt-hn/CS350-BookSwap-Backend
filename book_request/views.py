from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from book.models import Book
from book.serializers import BookSerializer
# Create your views here.

@api_view(['GET'])
def book_request_sent(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            books = Book.objects.filter(requester=request.user.id)
            serializer = BookSerializer(books, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def book_request_received(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            books = Book.objects.filter(current_owner=request.user.id) & Book.objects.filter(requested=True)
            serializer = BookSerializer(books, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def book_request_ongoing(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            books = Book.objects.filter(current_owner=request.user.id, ongoing=True) | Book.objects.filter(requester = request.user.id, ongoing=True)
            serializer = BookSerializer(books, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
