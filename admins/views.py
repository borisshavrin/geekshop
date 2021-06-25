from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm
from users.models import User


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


# CRUD
class AdminUsersListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUsersListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(AdminUsersListView, self).dispatch(request, *args, **kwargs)


class AdminUsersCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')
    success_message = 'Пользователь создан!'

    def get_context_data(self, **kwargs):
        context = super(AdminUsersCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Регистрация'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(AdminUsersCreateView, self).dispatch(request, *args, **kwargs)


class AdminUsersUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    success_message = 'Данные успешно изменены!'

    def get_context_data(self, **kwargs):
        context = super(AdminUsersUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Обновление пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(AdminUsersUpdateView, self).dispatch(request, *args, **kwargs)


class AdminUsersDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')
    success_message = 'Пользователь удален!'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AdminUsersDeleteView, self).dispatch(request, *args, **kwargs)


class AdminUsersReturnView(AdminUsersDeleteView):
    success_message = 'Пользователь восстановлен!'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(AdminUsersReturnView, self).dispatch(request, *args, **kwargs)
