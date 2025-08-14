from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Tip

class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(Tip)
admin.site.register(CustomUser, CustomUserAdmin)


