from django.contrib import admin

from users.models import User, UserProfile
from basket.admin import BasketAdmin


class UserProfileAdmin(admin.TabularInline):
    model = UserProfile
    fields = ('tagline', 'gender', 'about_me')
    extra = 0       # удаляем доп поля


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (BasketAdmin,         # Отображение карзины пользователя на админ-панели информации о пользователе
               UserProfileAdmin,)   # доп профиль пользователя
