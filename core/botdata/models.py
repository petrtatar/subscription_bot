from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(unique=True, null=True)
    username = models.CharField(max_length=600, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pk}"


class Tariff(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(null=False)
    days = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name}"
