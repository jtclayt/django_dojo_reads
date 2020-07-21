from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as logout_user
from django.contrib.auth import get_user_model

from .forms import LoginForm, RegisterForm


def index(request):
    return redirect(reverse('users:login'))


class Main(object):
    template = None
    context = None

    def get(self, request):
        return render(request, self.get_template(), self.get_context())

    def get_template(self):
        if self.template is not None:
            return self.template
        raise ImproperlyConfigured('Template not defined.')

    def get_context(self):
        if self.context is not None:
            return self.context
        raise ImproperlyConfigured('Context not defined.')


class Login(Main, View):
    template = 'login.html'
    context = {
        'login_form': LoginForm()
    }

    def post(self, request, *args, **kwargs):
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect(reverse('app:index'))
        messages.error(request, 'Invalid credentials')
        return redirect(reverse('users:login'))


class Register(Main, View):
    template = 'register.html'
    context = {
        'reg_form': RegisterForm()
    }

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = get_user_model().objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                alias=form.cleaned_data['alias']
            )
            login(request, user)
            print(request.user.is_authenticated)
            return redirect('app:index')
        for key, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)
        return redirect(reverse('users:register'))


def logout(request):
    logout_user(request)
    return redirect(reverse('users:login'))


def check_alias(request, alias):
    if len(get_user_model().objects.filter(alias=alias)) == 0:
        return HttpResponse('available')
    return HttpResponse('unavailable')
