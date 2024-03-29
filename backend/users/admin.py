from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class MyUserAdmin(UserAdmin):
    change_user_password_template = True
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_superuser', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
