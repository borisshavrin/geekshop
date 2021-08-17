from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.db.models import F

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, UserAdminProductCategoryEditForm
from products.models import ProductCategory
from users.models import User


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


class AdminUsersCategoryListView(ListView):
    model = ProductCategory
    template_name = 'admins/categories.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUsersCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(AdminUsersCategoryListView, self).dispatch(request, *args, **kwargs)


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


def db_profile_by_type(prefix, type, queries):
    """Ф-ия отфильтровывает запросы определенного типа (например, «UPDATE», «DELETE», «SELECT», «INSERT INTO»)"""
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    """Вместо работы с методами классов «ProductCategoryUpdateView()» и «ProductCategoryDeleteView()»
        воспользовались механизмом сигналов - так будет меньше кода.  Атрибут «product_set Django»
        создан автоматически для связи с моделью Product по внешнему ключу. В этом атрибуте получаем QuerySet,
        который позволяет получить все продукты в данной категории и применяем к нему метод «.update()»."""
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)


class AdminUserProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'admins/category_update.html'
    success_url = reverse_lazy('admins:categories')
    form_class = UserAdminProductCategoryEditForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUserProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Категории/Редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set. \
                    update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)
