from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from category.views import CategoryListView, CategoryDetailView


class TestCategoryUrls(APITestCase):
    def test_category_list_url_is_resolved(self):
        url = reverse("category:category_list")
        self.assertEquals(resolve(url).func.view_class, CategoryListView)

    def test_category_detail_url_is_resolved(self):
        url = reverse("category:category_detail", args=[1])
        self.assertEquals(resolve(url).func.view_class, CategoryDetailView)
