from django.urls import path
from . import views

urlpatterns = [
    path('sent/', views.book_request_sent,name="book_request_sent"),
    path('received/', views.book_request_received,name="book_request_received"),
    path('ongoing/', views.book_request_ongoing,name="book_request_ongoing"),
]
