from django.urls import path
from . import views

urlpatterns = [
    path('sent/', views.book_request_sent,name="book_request_sent"),
    path('received/', views.book_request_received,name="book_request_received"),
    path('ongoing/', views.book_request_ongoing,name="book_request_ongoing"),
    path('request_book/<int:id>/', views.send_book_request,name="send_book_request"),
    path('accept_book/<int:id>/', views.accept_book_request, name="accept_book_request"),
    path('reject_book/<int:id>/', views.reject_book_request, name="reject_book_request"),
]
