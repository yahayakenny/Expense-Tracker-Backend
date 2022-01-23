from expense.models import Expense
from core.helpers import AuthenticateUser
from core.helpers import today, tomorrow


class TestExpenseModel(AuthenticateUser):
    def test_expense_total(self):
        user = self.authenticate_user()
        test_expense_one = Expense.objects.create(
            name="new expense", amount=400, description="new expense description"
        )
        test_expense_two = Expense.objects.create(
            name="new expense 2", amount=900, description="new expense description 2"
        )
        test_expense_three = Expense.objects.create(
            name="new expense 3", amount=1300, description="new expense description 3"
        )
        total_expense_filtered_today = Expense.get_expense_total(today, today, user)
        total_expense_filtered_tomorrow = Expense.get_expense_total(tomorrow, tomorrow, user)
        self.assertEquals(total_expense_filtered_today, 2600)
        self.assertEquals(total_expense_filtered_tomorrow, 0)

    def 