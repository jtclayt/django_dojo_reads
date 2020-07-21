from django.urls import path
from .views import index, BooksView

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('books/', BooksView.as_view(), name='books')
]
