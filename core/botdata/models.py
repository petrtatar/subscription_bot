from django.db import models


class UserProfile(models.Model):
    id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}"


class Tariffs(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(null=False)
    days = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name}"
