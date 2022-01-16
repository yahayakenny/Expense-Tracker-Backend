from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Income(models.Model):
    name = models.CharField(max_length=30,blank=True, null=True)
    amount = models.FloatField(default = 0, blank=True)
    user = models.ForeignKey(User,related_name = 'incomes', on_delete=models.SET_NULL, null = True )
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name

