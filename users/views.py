from django.shortcuts import render
from users.forms import UserLoginForm


def login(request):
    form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация',
               'form': form
               }
    return render(request, 'users/login.html', context)


def register(request):
    context = {'title':
               'GeekShop - Регистрация'}
    return render(request, 'users/register.html', context)
