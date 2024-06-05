from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Book
from .serializers import BookSerializer
from account_api.models import User
# Create your views here.

@parser_classes([MultiPartParser, FormParser])
@api_view(['GET', 'POST'])
def book_list(request, format=None):
    if request.method == 'GET':
        books = Book.objects.exclude(isPrivate=True)
        serializer = BookSerializer(books, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            request.data['current_owner'] = request.user.id
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({'Error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if request.user.is_authenticated and book.current_owner == request.user:
            mutable_data = request.data.copy()
            if not 'current_owner' in mutable_data:
                mutable_data['current_owner']= request.user.id
            serializer = BookSerializer(book, data=mutable_data)
            if serializer.is_valid():
                if "image" not in request.FILES:
                    serializer.validated_data["image"] = book.image
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if request.user.is_authenticated and book.current_owner == request.user:
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Error': 'Authentication credentials were not provided or user not owner.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def search_book_by_title(request):
    title = request.data.get('title', None)
    author = request.data.get('author', None)
    if not title and not author:
        return Response({'Error': 'At least one of title or author parameters is required'}, status=status.HTTP_400_BAD_REQUEST)
    filter_criteria = {}
    if title:
        filter_criteria['title__icontains'] = title
    if author:
        filter_criteria['author__icontains'] = author
    filter_criteria['isPrivate'] = False
    books = Book.objects.filter(**filter_criteria)
    serializer = BookSerializer(books, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_books(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_books = Book.objects.filter(current_owner=current_user)
        serializer = BookSerializer(user_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'Error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def user_private_books(request):
    if request.user.is_authenticated:
        current_user = request.user
        private_books = Book.objects.filter(current_owner=current_user, isPrivate=True)
        serializer = BookSerializer(private_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'Error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])   
def user_public_books(request):
    if request.user.is_authenticated:
        current_user = request.user
        public_books = Book.objects.filter(current_owner=current_user, isPrivate=False)
        serializer = BookSerializer(public_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'Error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])   
def get_user_books(request, id):
    if request.user.is_authenticated:
        user = User.objects.filter(id=id)[0]
        user_books = Book.objects.filter(current_owner = user)
        serializer = BookSerializer(user_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'Error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
