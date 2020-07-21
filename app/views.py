from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    return redirect(reverse('app:books'))


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
        return redirect(reverse('app:books'))
