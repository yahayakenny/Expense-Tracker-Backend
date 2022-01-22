from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from expense.views import ExpenseListView, ExpenseDetailView


class TestExpenseUrls(APITestCase):
    def test_expense_list_url_is_resolved(self):
        url = reverse("expense:expense_list")
        self.assertEquals(resolve(url).func.view_class, ExpenseListView)

    def test_expense_detail_url_is_resolved(self):
        url = reverse("expense:expense_detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, ExpenseDetailView)
