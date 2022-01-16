from rest_framework import serializers

from expense.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "user", "name", "description", "amount", "date", "category"]
        depth = 1


