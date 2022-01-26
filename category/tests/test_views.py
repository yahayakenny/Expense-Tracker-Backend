from rest_framework import status
from core.helpers import AuthenticateUser
from category.models import Category

from django.urls import reverse


class TestCategoryView(AuthenticateUser):
    def create_category(self):
        sample_category = {"name": "new category"}
        response = self.client.post(reverse("category:category_list"), sample_category)
        return response

    def test_cannot_retrieve_category_list_without_auth(self):
        response = self.client.get(reverse("category:category_list"))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_retrieve_category_detail_without_auth(self):
        response = self.client.get(reverse("category:category_detail", args=[1]))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_create_category_without_auth(self):
        response = self.client.post(reverse("category:category_list"))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_category_with_auth(self):
        self.authenticate_user()
        response = self.create_category()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data["name"], "new category")

    def test_can_retrive_category_list_with_auth(self):
        self.authenticate_user()
        response = self.client.get(reverse("category:category_list"))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_can_retrieve_category_detail_with_auth(self):
        self.authenticate_user()
        response = self.create_category()
        res = self.client.get(reverse("category:category_detail", args=[response.data["id"]]))
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        category = Category.objects.get(id=response.data["id"])
        self.assertEquals(category.name, res.data["name"])

    def test_can_edit_category(self):
        self.authenticate_user()
        response = self.create_category()
        res = self.client.put(
            reverse("category:category_detail", args=[response.data["id"]]),
            {"name": "updated category"},
        )
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_can_delete_category(self):
        self.authenticate_user()
        response = self.create_category()
        prev_category_count = Category.objects.all().count()
        res = self.client.delete(reverse("category:category_detail", args=[response.data["id"]]))
        current_category_count = Category.objects.all().count()
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertGreater(prev_category_count, current_category_count)
