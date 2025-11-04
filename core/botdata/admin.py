from django.contrib import admin
from .models import (UserProfile, Tariffs)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone')


@admin.register(Tariffs)
class TariffsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'days')
