from django.contrib import admin
from .models import (UserProfile, Tariff,
                     Broadcast, Subscription,
                     Transaction)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone')


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration_days')


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at', 'send_at', 'sent')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tariff', 'start_date', 'end_date', 'is_active')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tariff', 'amount', 'status', 'payment_id', 'created_at')
