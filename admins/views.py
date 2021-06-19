from django.shortcuts import render

from users.models import User


def index(request):
    return render(request, 'admins/admin.html')


# CRUD
def admin_users(request):
    context = {'users': User.objects.all()}
    return render(request, 'admins/admin-users-read.html', context)


def admin_users_create(request):
    return render(request, 'admins/admin-users-create.html')


def admin_users_update(request, id):
    return render(request, 'admins/admin-users-update-delete.html')


def admin_users_delete(request, id):
    pass
