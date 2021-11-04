from rest_framework import serializers
from expense.models import Category, Expense
from rest_framework import serializers

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Expense
        fields = ['id','user' ,'name', 'description', 'amount', 'date', 'category' ]
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','user', 'name']
        depth = 1 
