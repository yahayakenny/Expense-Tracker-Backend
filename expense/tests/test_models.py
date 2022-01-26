from expense.models import Expense
from core.helpers import AuthenticateUser
from core.constants import today, tomorrow
from income.models import Income


class TestExpenseModel(AuthenticateUser):
    def setUp(self):
        Expense.objects.create(
            name="new expense", amount=400, description="new expense description"
        )
        Expense.objects.create(
            name="new expense 2", amount=900, description="new expense description 2"
        )
        Expense.objects.create(
            name="new expense 3", amount=1200, description="new expense description 3"
        )
        Income.objects.create(
            name="new income", amount=4000, description="new income description"
        )
        Income.objects.create(
            name="new income 2", amount=3000, description="new income description 2"
        )
        Income.objects.create(
            name="new income 3", amount=2000, description="new income description 3"
        )

    def test_expense_total(self):
        user = self.authenticate_user()
        test_expense_one = Expense.objects.get(name="new expense")
        test_expense_two = Expense.objects.get(name="new expense 2")
        test_expense_three = Expense.objects.get(name="new expense 3")
        total_expense_filtered_today = Expense.get_expense_total(today, today, user)
        total_expense_filtered_tomorrow = Expense.get_expense_total(
            tomorrow, tomorrow, user
        )
        self.assertEquals(total_expense_filtered_today, 2500)
        self.assertEquals(total_expense_filtered_tomorrow, 0)

    def test_expenses_daily_for_the_week(self):
        user = self.authenticate_user()
        test_expense_one = Expense.objects.get(name="new expense")
        test_expense_two = Expense.objects.get(name="new expense 2")
        test_expense_three = Expense.objects.get(name="new expense 3")
        filtered = Expense.get_expenses_daily_for_the_week(user)
        self.assertEquals(filtered[-1]["amount"], 2500)

    def test_expenses_monthly_for_the_year(self):
        user = self.authenticate_user()
        test_expense_one = Expense.objects.get(name="new expense")
        test_expense_two = Expense.objects.get(name="new expense 2")
        test_expense_three = Expense.objects.get(name="new expense 3")
        filtered = Expense.get_expenses_monthly_for_the_year(user)
        self.assertEquals(filtered[0]["month"], "January")
        self.assertEquals(filtered[0]["amount"], 2500)

    def test_net_expenses_for_the_month(self):
        user = self.authenticate_user()
        test_expense_one = Expense.objects.get(name="new expense")
        test_expense_two = Expense.objects.get(name="new expense 2")
        test_expense_three = Expense.objects.get(name="new expense 3")
        test_income_one = Income.objects.get(name="new income")
        test_income_two = Income.objects.get(name="new income 2")
        test_income_three = Income.objects.get(name="new income 3")
        filtered = Expense.get_net_expenses_for_the_month(user)
        self.assertEquals(filtered[0]["expense"], 2500)
        self.assertEquals(filtered[0]["income"], 9000)
        self.assertEquals(filtered[0]["net"], 6500)
        self.assertEquals(filtered[0]["incomeCount"], 3)
        self.assertEquals(filtered[0]["expenseCount"], 3)
