from django.contrib import admin
from api.models import User, Capsule

# Register your models here.


class UserAdm(admin.ModelAdmin):
    list_display = ('user', 'id', 'name', 'profile', 'created_at', 'updated_at', 'is_active')
    ordering = ['-created_at']
    

class CapsuleAdm(admin.ModelAdmin):
    list_display = ('flavor', 'id', 'price_cost', 'price_sale', 'cod_vendor', 'created_at', 'updated_at', 'is_active')
    ordering = ['-created_at']


admin.site.register(User, UserAdm)
admin.site.register(Capsule, CapsuleAdm)