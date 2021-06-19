from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from admins.forms import UserAdminRegisterForm
from users.models import User


def index(request):
    return render(request, 'admins/admin.html')


# CRUD
def admin_users(request):
    context = {'title': 'GeekShop - Админ | Пользователи',
               'users': User.objects.all()}
    return render(request, 'admins/admin-users-read.html', context)


def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegisterForm()
    context = {'title': 'GeekShop - Админ | Регистрация', 'form': form}
    return render(request, 'admins/admin-users-create.html', context)


def admin_users_update(request, id):
    return render(request, 'admins/admin-users-update-delete.html')


def admin_users_delete(request, id):
    pass
