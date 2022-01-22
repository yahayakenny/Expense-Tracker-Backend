from expense.models import Expense
from core.helpers import AuthenticateUser
from core.helpers import today, tomorrow


class ExpenseModelTest(AuthenticateUser):
    def test_expense_total(self):
        user = self.authenticate_user()
        test_expense_one = Expense.objects.create(
            name="new expense", amount=400, description="new expense description"
        )
        test_expense_two = Expense.objects.create(
            name="new expense 2", amount=900, description="new expense description 2"
        )
        test_expense_two = Expense.objects.create(
            name="new expense 3", amount=1400, description="new expense description 3"
        )
        queryset = Expense.objects.all()
        total_expense = sum([expense.amount for expense in queryset])
        total_expense_filtered_today = Expense.get_expense_total(today, today, user)
        total_expense_filtered_tomorrow = Expense.get_expense_total(tomorrow, tomorrow, user)
        self.assertEquals(Expense.objects.all().count(), 3)
        self.assertNotEqual(test_expense_one.amount, test_expense_two.amount)
        self.assertEquals(total_expense, 2700)
        self.assertEquals(total_expense_filtered_today, 2700)
        self.assertEquals(total_expense_filtered_tomorrow, 0)

