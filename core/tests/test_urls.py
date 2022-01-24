from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from core.views import QueryNetView 


class TestCoreUrls(APITestCase):
    def test_new_view_url_is_resolved(self):
        url = reverse("core:query_net")
        self.assertEquals(resolve(url).func.view_class, QueryNetView)

