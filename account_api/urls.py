from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('register/',views.register_api, name='register_api'),
    path('user/',views.user_api, name='user_api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get_user/', views.get_user_from_id(), name="get_user")
]
