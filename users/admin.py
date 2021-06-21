from django.contrib import admin

from users.models import User
from basket.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (BasketAdmin,)        # Отображение карзины пользователя на админ-панели информации о пользователе
