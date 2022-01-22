from rest_framework import status
from core.helpers import AuthenticateUser
from income.models import Income

from django.urls import reverse


class TestIncomeView(AuthenticateUser):
    def create_income(self):
        sample_income = {"name": "new income", "amount": 400, "description": "a sample income"}
        response = self.client.post(reverse("income:income_list"), sample_income)
        return response

    def test_cannot_retrieve_income_list_without_auth(self):
        response = self.client.get(reverse("income:income_list"))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_retrieve_income_detail_without_auth(self):
        response = self.client.get(reverse("income:income_detail", args=[1]))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_create_income_without_auth(self):
        response = self.client.post(reverse("income:income_list"))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_income_with_auth(self):
        previous_income_count = Income.objects.all().count()
        self.authenticate_user()
        response = self.create_income()
        self.assertEquals(Income.objects.all().count(), previous_income_count + 1)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data["name"], "new income")
        self.assertEquals(response.data["amount"], 400)
        self.assertEquals(response.data["description"], "a sample income")

    def test_can_retrive_income_list_with_auth(self):
        self.authenticate_user()
        response = self.client.get(reverse("income:income_list"))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_can_retrieve_income_detail_with_auth(self):
        self.authenticate_user()
        response = self.create_income()
        res = self.client.get(reverse("income:income_detail", args=[response.data["id"]]))
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        income = Income.objects.get(id=response.data["id"])
        self.assertEquals(income.name, res.data["name"])

    def test_can_edit_income(self):
        self.authenticate_user()
        response = self.create_income()
        res = self.client.put(
            reverse("income:income_detail", args=[response.data["id"]]),
            {"name": "updated income", "amount": 600, "description": "an updated sample income"},
        )
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_can_delete_income(self):
        self.authenticate_user()
        response = self.create_income()
        prev_income_count = Income.objects.all().count()
        res = self.client.delete(reverse("income:income_detail", args=[response.data["id"]]))
        current_income_count = Income.objects.all().count()
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertGreater(prev_income_count, current_income_count)
