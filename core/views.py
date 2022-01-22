from category.models import Category
from expense.models import Expense
from expense.serializers import ExpenseSerializer
from income.models import Income
from income.serializers import IncomeSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import INCOME, EXPENSE, current_month
from core.helpers import get_trunc_week


# Get all expenses for a date range(from_date and to_date on front end)
class QueryDateRangeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        select = request.GET.get("select")
        if select == EXPENSE:
            filtered_expense = (
                Expense.objects.filter(user=request.user)
                .filter(date__range=(from_date, to_date))
                .order_by("-id")
            )
            serializer = ExpenseSerializer(filtered_expense, many=True)
            expense_sum = Expense.get_expense_total(from_date, to_date, select, request.user)
            json_data = {"filtered": serializer.data, "total": expense_sum}
            try:
                if json_data:
                    return Response(json_data, status=status.HTTP_200_OK)
            except:
                return Response(
                    data={"message": "Results not found, Invalid parameters"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        if select == INCOME:
            filtered_income = (
                Income.objects.filter(user=request.user)
                .filter(date__range=(from_date, to_date))
                .order_by("-id")
            )
            serializer = IncomeSerializer(filtered_income, many=True)
            income_sum = Income.get_income_total(from_date, to_date, select, request.user)
            json_data = {"filtered": serializer.data, "total": income_sum}
            try:
                if json_data:
                    return Response(json_data, status=status.HTTP_200_OK)
            except:
                return Response(
                    data={"message": "Results not found, Invalid parameters"},
                    status=status.HTTP_404_NOT_FOUND,
                )


# last 7 days
class QueryDayGraph(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            return Response(
                {"filtered": Expense.get_expenses_daily_for_the_week(request.user)},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                data={"message": "Unable to get daily expenses for the last week"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Query each week of the month
class QueryWeekGraph(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            return Response(get_trunc_week(user=request.user), status=status.HTTP_200_OK)

        except:
            return Response(
                data={"message": "Unable to get expenses for each week of the month"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Monthly Expenses
class QueryMonthGraph(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            return Response(Expense.get_expenses_monthly_for_the_year(request.user))
        except:
            return Response(
                data={"message": "Unable to get monthly expenses for the year"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class QueryMostRecentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            filtered = (
                Expense.objects.filter(user=request.user)
                .filter(date__month=str(current_month))
                .order_by("-id")[:5]
            )
            serializer = ExpenseSerializer(filtered, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get most recent expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class QueryNetView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            category_count = (
                Category.objects.filter(user=request.user)
                .filter(date__month=str(current_month))
                .all()
                .count()
            )

            data = Expense.get_net_expenses_for_the_month(request.user)
            data[0]["categoryCount"] = category_count
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to get net expenses"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class QueryCategoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            categories = Category.objects.filter(user=request.user).filter(
                date__month=str(current_month)
            )
            data = []
            for i in categories:
                data.append({"category": i.name, "amount": i.total_expense_cost})
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to group by categories"},
                status=status.HTTP_400_BAD_REQUEST,
            )
