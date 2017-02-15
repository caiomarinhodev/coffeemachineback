from django.contrib import admin
from api.models import User

# Register your models here.


class UserAdm(admin.ModelAdmin):
    list_display = ('user', 'id', 'name', 'profile', 'created_at', 'updated_at', 'is_active')
    ordering = ['-created_at']


admin.site.register(User, UserAdm)