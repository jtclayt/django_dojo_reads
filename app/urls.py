from django.urls import path
from .views import index, new_book, BooksView, BookDetailView

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('books/', BooksView.as_view(), name='books'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('books/new/', new_book, name='new_book')
]
