from django.contrib import admin

from api_apps.cart.models import UserCart


# Register your models here.

@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    pass
