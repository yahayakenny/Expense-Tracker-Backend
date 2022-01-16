from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Expense(models.Model):
    user = models.ForeignKey(User, related_name="expenses", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    amount = models.FloatField(default=0, blank=True)
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
