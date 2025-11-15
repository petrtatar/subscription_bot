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
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(null=False)
    duration_days = models.IntegerField(null=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"


class Broadcast(models.Model):
    text = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to="broadcasts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    send_at = models.DateTimeField(blank=True, null=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Рассылка {self.pk} ({'Отправлена' if self.sent else 'в очереди'})"


class Subscription(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def activate(self, tariff: Tariff):
        now = timezone.now()

        if self.is_active and self.end_date and self.end_date > now:
            self.start_date = now
            self.end_date = self.end_date + timezone.timedelta(days=tariff.duration_days)
        else:
            self.start_date = now
            self.end_date = now + timezone.timedelta(days=tariff.duration_days)

        self.tariff = tariff
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.pk}"


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('paid', 'Оплачено'),
        ('failed', 'Ошибка')
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}"
