import django.contrib.messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from geekshop import settings
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
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
    success_message = 'Вы успешно зарегистрировались, проверьте почту для подтверждения!'

    def get_context_data(self, **kwargs):
        context = super(UsersRegisterViews, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учетной записи {user.username}'
        message = f'\nДля подтверждения Вашей учетной записи {user.email} на портале {settings.DOMAIN_NAME}' \
                  f'перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
        self.success_message += message
        send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        return super(UsersRegisterViews, self).form_valid(form)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'users/verification.html')
        else:
            print(f'error activation user {user.username}')
            return render(request, 'users/verification.html')
    except Exception as err:
        print(f'error activation user {err.args}')
        return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class UsersProfileView(SuccessMessageMixin, UpdateView):
    template_name = 'users/profile.html'
    success_url = 'users:profile'
    success_message = 'Данные успешно изменены!'
    form_class = UserProfileForm
    model = User

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'userprofileform': UserProfileForm(prefix='userprofileform_pre', instance=request.user),
             'userprofileeditform': UserProfileEditForm(prefix='userprofileeditform_pre',
                                                        instance=request.user.userprofile)})

    def get_context_data(self, **kwargs):
        context = super(UsersProfileView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            userprofileform = UserProfileForm(
                self.request.POST, instance=self.request.user, prefix='userprofileform_pre')
            userprofileeditform = UserProfileEditForm(
                self.request.POST, instance=self.request.user.userprofile, prefix='userprofileeditform_pre')

            if userprofileform.is_valid() and userprofileeditform.is_valid():
                userprofileform.save()
                return HttpResponseRedirect(reverse('users:profile'))
        else:
            userprofileform = UserProfileForm(instance=self.request.user)
            userprofileeditform = UserProfileEditForm(instance=self.request.user.userprofile)

        context['title'] = 'GeekShop - Личный кабинет'
        context['userprofileform'] = userprofileform
        context['userprofileeditform'] = userprofileeditform
        context['basket'] = Basket.objects.filter(user=self.get_object())
        return context

    def get_success_url(self):
        return reverse_lazy(self.success_url, args=(self.request.user.id,))

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(UsersProfileView, self).dispatch(request, *args, **kwargs)
