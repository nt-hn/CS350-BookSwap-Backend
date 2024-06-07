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
    

@api_view(['POST'])
def send_book_request(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                book = Book.objects.get(id=id)
                if book.requested:
                    return Response({'Error': 'Book is already requested.'}, status=status.HTTP_226_IM_USED)
                
                book.requested = True
                book.requester = request.user
                book.save()

                serializer = BookSerializer(book)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Book.DoesNotExist:
                print("book not found")
                return Response({'Error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'Error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def accept_book_request(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                book = Book.objects.get(id=id)
                if not book.requested:
                    return Response({'Error': 'Book is not requested.'}, status=status.HTTP_226_IM_USED)
                
                book.requested = False
                book.ongoing = True
                book.save()

                serializer = BookSerializer(book)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Book.DoesNotExist:
                return Response({'Error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'Error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def reject_book_request(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                book = Book.objects.filter(id=id)[0]
                
                book.requester = None
                book.requested = False
                book.ongoing = False
                book.save()

                serializer = BookSerializer(book)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Book.DoesNotExist:
                return Response({'Error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'Error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)
