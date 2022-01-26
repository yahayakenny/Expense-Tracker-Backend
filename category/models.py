from django.contrib.auth.models import User
from django.db import models
from expense.models import Expense
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, related_name="categories", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    @property
    def total_expense_cost(self):
        expenses = Expense.objects.all().filter(category=self.id)
        return sum([expense.amount for expense in expenses])


# Signals that create default categories automatically on creating a new user
@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs) -> None:
    if created:
        Category.objects.create(user=instance, name="feeding")
        Category.objects.create(user=instance, name="clothing")
        Category.objects.create(user=instance, name="transport")
        Category.objects.create(user=instance, name="bills")
        Category.objects.create(user=instance, name="others")

