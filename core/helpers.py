from django.db.models import Sum
from django.db.models.functions import TruncWeek
from expense.models import Expense


def get_trunc_week(user):
    filtered = (
        Expense.objects.all()
        .filter(user=user)
        .annotate(week=TruncWeek("date"))
        .values("week")
        .annotate(total=Sum("amount"))
        .order_by("week")
    )
    data = {"filtered": filtered}
    return data
