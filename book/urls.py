from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list,name="book_list"),
    path('<int:id>/', views.book_detail,name="book_detail"),
    path('search_book_by_title/', views.search_book_by_title, name='search_book_by_title'),
    path('user_books/', views.user_books, name="user_books"),
    path('user_books/private/', views.user_private_books, name="user_books_private"),
    path('user_books/public/', views.user_public_books, name="user_books_public"),
]
