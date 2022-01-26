from income.models import Income
from core.helpers import AuthenticateUser
from core.constants import today


class IncomeModelTest(AuthenticateUser):
    def test_income_total(self):
        user = self.authenticate_user()
        test_income_one = Income.objects.create(
            name="new income", amount=400, description="new income description"
        )
        test_income_two = Income.objects.create(
            name="new income 2", amount=900, description="new income description 2"
        )
        test_income_two = Income.objects.create(
            name="new income 3", amount=1400, description="new income description 3"
        )
        queryset = Income.objects.all()
        total_income = sum([income.amount for income in queryset])
        total_income_filtered = Income.get_income_total(today, today, user)
        self.assertEquals(Income.objects.all().count(), 3)
        self.assertNotEqual(test_income_one.amount, test_income_two.amount)
        self.assertEquals(total_income, 2700)
        self.assertEquals(total_income_filtered, 2700)
