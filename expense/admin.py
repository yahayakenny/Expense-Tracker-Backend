from django.contrib import admin

from expense.models import Category, Expense

# Register your models here.
admin.site.register(Expense)
admin.site.register(Category)