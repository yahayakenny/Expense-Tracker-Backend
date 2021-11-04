from rest_framework.serializers import ModelSerializer
from income.models import Income

class IncomeSerializer(ModelSerializer):
    class Meta: 
        model = Income
        fields = ['id','user', 'name', 'description', 'amount', 'date',]
        depth = 2
