from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Author, Book, Review


def index(request):
    return redirect(reverse('app:books'))


def new_book(request):
    context = {'authors': Author.objects.all()}
    return render(request, 'new-book.html', context)


class Main(object):
    template = None

    def get_template(self):
        if self.template is not None:
            return self.template
        raise ImproperlyConfigured('Template not defined.')


class BooksView(LoginRequiredMixin, Main, View):
    login_url = '/users/login/'
    template = 'books.html'

    def get(self, request):
        return render(request, self.get_template())

    def post(self, request):
        errors = Review.objects.validator(request.POST)
        if len(errors) > 0:
            for error in errors.items():
                messages.error(request, error)
            return redirect(reverse('app:new_book'))

        if len(request.POST['author']) > 0:
            author = Author.objects.get_or_create(
                name__iexact=request.POST['author']
            )
        else:
            author = get_object_or_404(Author, id=request.POST['author_id'])

        book = Book.objects.create(title=request.POST['title'], author=author)
        Review.objects.create(
            review=request.POST['review'],
            rating=int(request.POST['rating']),
            book=book,
            created_by=request.user
        )
        return redirect(reverse('app:books', args=(book.id,)))


class BookDetailView(LoginRequiredMixin, Main, View):
    login_url = '/users/login/'
    template = 'book-detail.html'

    def get(self, request, book_id):
        context = {'book': get_object_or_404(Book, id=book_id)}
        return render(request, self.get_template(), context)
