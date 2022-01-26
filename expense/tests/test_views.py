from core.helpers import AuthenticateUser
from django.urls import reverse
from rest_framework import status


class TestExpenseView(AuthenticateUser):
    def create_expense(self):
        sample_expense = {
            "name": "new expense",
            "amount": 600,
            "description": "a sample expense",
            "category": 1,
        }
        response = self.client.post(reverse("expense:expense_list"), sample_expense)
        return response

    def create_category(self):
        sample_category = {"name": "new category"}
        response = self.client.post(reverse("category:category_list"), sample_category)
        return response

    def test_cannot_retrieve_expense_list_without_auth(self):
        response = self.client.get(reverse("expense:expense_list"))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_retrieve_expense_detail_without_auth(self):
        response = self.client.get(reverse("expense:expense_detail", args=[1]))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_create_expense_without_auth(self):
        response = self.client.post(reverse("expense:expense_list"))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_expense_with_auth(self):
        self.authenticate_user()
        expense_response = self.create_expense()
        self.assertEquals(expense_response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(expense_response.data["name"], "new expense")
        self.assertEquals(expense_response.data["amount"], 600)
        self.assertEquals(expense_response.data["description"], "a sample expense")

    def test_can_retrive_expense_list_with_auth(self):
        self.authenticate_user()
        response = self.client.get(reverse("expense:expense_list"))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_can_edit_expense(self):
        self.authenticate_user()
        expense_response = self.create_expense()
        category_response = self.create_category()
        res = self.client.put(
            reverse("expense:expense_detail", args=[expense_response.data["id"]]),
            {
                "name": "updated expense",
                "amount": 600,
                "description": "an updated sample expense",
                "category": category_response.data["id"],
            },
        )
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_can_delete_expense(self):
        self.authenticate_user()
        test_expense = self.create_expense()
        test_expense_id = test_expense.data.get("id")
        url = "api/v1/users/" + str(test_expense_id) + "/"
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
