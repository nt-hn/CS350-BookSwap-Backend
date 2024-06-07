from rest_framework import response, status
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from . import models
# Create your views here.

@api_view(['POST'])
def register_api(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        instance = models.User()
        instance.first_name = data["first_name"]
        instance.last_name = data["last_name"]
        instance.email = data["email"]
        instance.set_password(data["password"])
        instance.save()
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_api(request):
    if request.user.is_authenticated:
        user = models.User.objects.filter(id=request.user.id).first()
        content = {'user_id': user.id, 'user_email': user.email, 'staff':user.is_staff, 'first_name':user.first_name, 'last_name':user.last_name}
        return response.Response(data=content, status=status.HTTP_200_OK)
    else:
        return response.Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])   
def get_user_from_id(request, id):
    if request.user.is_authenticated:
        user = models.User.objects.filter(id=id)[0]
        content = {'first_name':user.first_name, 'last_name':user.last_name, 'email': user.email}
        return response.Response(data=content, status=status.HTTP_200_OK)
    else:
        return response.Response({'Error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

