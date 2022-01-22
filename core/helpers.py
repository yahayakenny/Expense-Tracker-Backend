from django.db.models import Sum
from django.db.models.functions import TruncWeek
from expense.models import Expense
from django.urls import reverse
from rest_framework.test import APITestCase


def get_trunc_week(user):
    filtered = (
        Expense.objects.all()
        .filter(user=user)
        .annotate(week=TruncWeek("date"))
        .values("week")
        .annotate(total=Sum("amount"))
        .order_by("week")
    )
    data = {"filtered": filtered}
    return data


class AuthenticateUser(APITestCase):
    def authenticate_user(self):
        self.client.post(
            reverse("users:register"),
            {
                "first_name": "test",
                "last_name": "user",
                "email": "user@email.com",
                "username": "testuser",
                "password": "password",
            },
        )
        response = self.client.post(
            reverse("users:login"),
            {
                "username": "testuser",
                "password": "password",
            },
        )
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
