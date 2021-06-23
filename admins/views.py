from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm
from users.models import User


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


# CRUD
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
#     context = {'title': 'GeekShop - Админ | Пользователи',
#                'users': User.objects.all()}
#     return render(request, 'admins/admin-users-read.html', context)


class AdminUsersListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUsersListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Пользователи'
        return context

# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Пользователь создан!')
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminRegisterForm()
#     context = {'title': 'GeekShop - Админ | Регистрация', 'form': form}
#     return render(request, 'admins/admin-users-create.html', context)


class AdminUsersCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, **kwargs):
        context = super(AdminUsersCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Регистрация'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, id):
#     selected_user = User.objects.get(id=id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=selected_user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Данные успешно изменены!')
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=selected_user)
#     context = {
#         'title': 'GeekShop - Админ | Обновление пользователя',
#         'form': form,
#         'selected_user': selected_user,
#     }
#     return render(request, 'admins/admin-users-update-delete.html', context)


class AdminUsersUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, **kwargs):
        context = super(AdminUsersUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Обновление пользователя'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_delete(request, id):
#     user = User.objects.get(id=id)
#     user.is_active = False
#     user.save()
#     messages.success(request, 'Пользователь деактивирован!')
#     return HttpResponseRedirect(reverse('admins:admin_users'))


class AdminUsersDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_return(request, id):
#     user = User.objects.get(id=id)
#     user.is_active = True
#     user.save()
#     messages.success(request, 'Пользователь возобновлен!')
#     return HttpResponseRedirect(reverse('admins:admin_users'))

class AdminUsersReturnView(AdminUsersDeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
