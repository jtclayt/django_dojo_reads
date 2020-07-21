from django.urls import path
from .views import index, LoginView, RegisterView, check_alias, logout

app_name = 'users'

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('check-alias/<str:alias>', check_alias, name='check_alias')
]
