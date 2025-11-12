from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(unique=True, null=True)
    username = models.CharField(max_length=600, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    subscription_expires_at = models.DateTimeField(null=True, blank=True)
    bonus_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.pk}"


class Tariff(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(null=False)
    days = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name}"


class Broadcast(models.Model):
    text = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to="broadcasts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    send_at = models.DateTimeField(blank=True, null=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Рассылка {self.pk} ({'Отправлена' if self.sent else 'в очереди'})"
