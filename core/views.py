from rest_framework.response import Response
from rest_framework.views import APIView
from core.utils import get_trunc_week, one_week_ago, today, current_month
from expense.models import  Category, Expense
from expense.serializers import  ExpenseSerializer
from income.models import Income
from income.serializers import IncomeSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import calendar
from datetime import timedelta

#Get all expenses for a date range(from_date and to_date on front end)
class QueryDateRangeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        select = request.GET.get('select')
        def get_query(from_date, to_date, select):
            if select == 'expense':
                if from_date == to_date :
                    filtered_expense = Expense.objects.filter(user=request.user).filter(date=to_date)
                    serializer = ExpenseSerializer(filtered_expense, many = True)
                    expense_sum = round((sum(expense.amount  for expense in filtered_expense)), 2)
                    data =  {"filtered": serializer.data, "total": expense_sum}
                    return data
                else:
                    filtered_expense = Expense.objects.filter(user=request.user).filter(date__range = (from_date, to_date)).order_by('-id')
                    serializer = ExpenseSerializer(filtered_expense, many = True)
                    expense_sum = round((sum(expense.amount  for expense in filtered_expense)), 2)
                    data =  {"filtered": serializer.data, "total": expense_sum}
                    return data
            if select == 'income':
                if from_date == to_date :
                    filtered_income= Income.objects.filter(user=request.user).filter(date=to_date)
                    serializer = IncomeSerializer(filtered_income, many = True)
                    income_sum = round((sum(income.amount for income in filtered_income)), 2)
                    data =  {"filtered": serializer.data, "total": income_sum}
                    return data
                else:
                    filtered_income= Income.objects.filter(user=request.user).filter(date__range = (from_date, to_date)).order_by('-id')
                    serializer = IncomeSerializer(filtered_income, many = True)
                    income_sum = round((sum(income.amount for income in filtered_income)), 2)
                    data =  {"filtered": serializer.data, "total": income_sum}
                    return data
        json_data = get_query(from_date, to_date, select)
        if json_data:
            return Response(json_data, status=status.HTTP_200_OK)
        else: 
            return Response("ERROR", status=status.HTTP_404_NOT_FOUND)

#last 7 days
class QueryDayGraph(APIView):
    permission_classes = [IsAuthenticated]
    def get (self, request):
        data = [] 
        delta = today - one_week_ago  
        for i in range(delta.days + 1):
            day = one_week_ago + timedelta(days=i)
            queryset = Expense.objects.filter(user=request.user).filter(date__startswith = day)
            day_cost = sum([expense.amount for expense in queryset])
            data.append({"day": day,"amount": day_cost})
        return Response({"filtered": data})

#Query each week of the month
class QueryWeekGraph(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(get_trunc_week(user=request.user), status=status.HTTP_200_OK)

#Monthly Expenses
class QueryMonthGraph(APIView):
    permission_classes = [IsAuthenticated]
    def get (self, request):
        data = []
        for i in range(1, 13):
            months = Expense.objects.filter(user=request.user).filter(date__month = i)
            month_cost = sum([expense.amount for expense in months])
            month_name = calendar.month_name[i]
            data.append({"month": month_name,"amount": month_cost})
        return Response({"filtered": data})

class QueryMostRecentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        filtered = Expense.objects.filter(user=request.user).filter(date__month = str(current_month)).order_by('-id')[:5]
        serializer = ExpenseSerializer(filtered, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QueryNetView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        total_expenses = Expense.objects.filter(user=request.user).filter(date__month = str(current_month))
        expense_count = Expense.objects.filter(user=request.user).filter(date__month = str(current_month)).all().count()
       
        expense_sum = round((sum(expense.amount  for expense in total_expenses)), 2)
        total_income = Income.objects.filter(user=request.user).filter(date__month = str(current_month))
        income_count = Income.objects.filter(user=request.user).filter(date__month = str(current_month)).all().count()
      
        income_sum = round((sum(income.amount  for income in total_income)), 2)
        category_count = Category.objects.filter(user=request.user).filter(date__month = str(current_month)).all().count()

        net_value = income_sum-expense_sum
        return Response({"expense": expense_sum , "income": income_sum, "net":net_value, "incomeCount": income_count,"expenseCount": expense_count, "categoryCount":category_count }, status=status.HTTP_200_OK, )

class QueryCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = Category.objects.filter(user=request.user).filter(date__month = str(current_month))
        data = []
        for i in categories:
            data.append({"category": i.name,"amount": i.total_expense_cost})
        return Response({"filtered": data})


        