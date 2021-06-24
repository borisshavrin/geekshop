import django.contrib.messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User
from basket.models import Basket


class UsersLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super(UsersLoginView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Авторизация'
        return context


class UsersRegisterViews(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались!'

    def get_context_data(self, **kwargs):
        context = super(UsersRegisterViews, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context


# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Данные успешно изменены!')
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#     context = {
#         'title': 'GeekShop - Личный кабинет',
#         'form': form,
#         'basket': Basket.objects.filter(user=user),
#     }
#     return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class UsersProfileView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    success_message = 'Данные успешно изменены!'


    def get_context_data(self, **kwargs):
        context = super(UsersProfileView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Личный кабинет'
        context['basket'] = Basket.objects.filter(user=self.get_object())
        return context

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(UsersProfileView, self).dispatch(request, *args, **kwargs)
