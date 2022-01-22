from django.test import SimpleTestCase
from django.urls import reverse, resolve
from income.views import IncomeListView, IncomeDetailView


class TestIncomeUrls(SimpleTestCase):
    def test_income_list_url_is_resolved(self):
        url = reverse("income:income_list")
        self.assertEquals(resolve(url).func.view_class, IncomeListView)

    def test_income_detail_url_is_resolved(self):
        url = reverse("income:income_detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, IncomeDetailView)
