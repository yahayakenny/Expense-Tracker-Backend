from datetime import datetime, time, timedelta

from django.db.models import Sum
from django.db.models.functions import TruncWeek
from expense.models import Expense

today = datetime.now().date()
tomorrow = today + timedelta(1)
today_start = datetime.combine(today, time())
today_end = datetime.combine(tomorrow, time())
one_week_ago = today - timedelta(days=7)
one_month_ago=today-timedelta(days=30)
current_month = today.month

def get_trunc_week(user):
    filtered = Expense.objects.all().filter(user=user).annotate(week = TruncWeek('date')).values('week').annotate(total= Sum('amount')).order_by('week')
    data = {"filtered": filtered}
    return data
