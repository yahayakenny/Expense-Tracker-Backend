from datetime import datetime, time, timedelta

INCOME = "income"
EXPENSE = "expense"
today = datetime.now().date()
tomorrow = today + timedelta(1)
today_start = datetime.combine(today, time())
today_end = datetime.combine(tomorrow, time())
one_week_ago = today - timedelta(days=7)
one_month_ago = today - timedelta(days=30)
current_month = today.month
