from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Expense(models.Model):
    user = models.ForeignKey(User, related_name="expenses", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    amount = models.FloatField(default=0, blank=True)
    category = models.ForeignKey(
        "category.Category", on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_expense_total(from_date, to_date, user):
        if from_date == to_date:
            filtered_expense = Expense.objects.filter(user=user).filter(date=to_date)
            expense_sum = round((sum(expense.amount for expense in filtered_expense)), 2)
            return expense_sum
        else:
            filtered_expense = (
                Expense.objects.filter(user=user)
                .filter(date__range=(from_date, to_date))
                .order_by("-id")
            )
            expense_sum = round((sum(expense.amount for expense in filtered_expense)), 2)
            return expense_sum
