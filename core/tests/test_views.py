from core.helpers import AuthenticateUser
from django.urls import reverse


class TestCoreView(AuthenticateUser):
    def test_user_can_query_day_graph_with_auth(self):
        user = self.authenticate_user()
        response = self.client.get(reverse("core:query_day_graph"))
        self.assertEquals(response.status_code, 200)

    def test_user_cannot_query_day_graph_without_auth(self):
        response = self.client.get(reverse("core:query_day_graph"))
        self.assertEquals(response.status_code, 401)

    def test_user_can_query_week_graph_with_auth(self):
        user = self.authenticate_user()
        response = self.client.get(reverse("core:query_week_graph"))
        self.assertEquals(response.status_code, 200)

    def test_user_cannot_query_week_graph_without_auth(self):
        response = self.client.get(reverse("core:query_week_graph"))
        self.assertEquals(response.status_code, 401)

    def test_user_can_query_month_graph_with_auth(self):
        user = self.authenticate_user()
        response = self.client.get(reverse("core:query_month_graph"))
        self.assertEquals(response.status_code, 200)

    def test_user_cannot_query_month_graph_without_auth(self):
        response = self.client.get(reverse("core:query_month_graph"))
        self.assertEquals(response.status_code, 401)

    def test_user_can_query_category_with_auth(self):
        user = self.authenticate_user()
        response = self.client.get(reverse("core:query_category"))
        self.assertEquals(response.status_code, 200)

    def test_user_cannot_query_category_without_auth(self):
        response = self.client.get(reverse("core:query_category"))
        self.assertEquals(response.status_code, 401)

    def test_user_can_query_most_recent_expenses_with_auth(self):
        user = self.authenticate_user()
        response = self.client.get(reverse("core:query_most_recent_expenses"))
        self.assertEquals(response.status_code, 200)

    def test_user_cannot_query_most_recent_expenses_without_auth(self):
        response = self.client.get(reverse("core:query_most_recent_expenses"))
        self.assertEquals(response.status_code, 401)

    def test_user_can_query_net_with_auth(self):
        user = self.authenticate_user()
        response = self.client.get(reverse("core:query_net"))
        self.assertEquals(response.status_code, 200)

    def test_user_cannot_query_net_without_auth(self):
        response = self.client.get(reverse("core:query_net"))
        self.assertEquals(response.status_code, 401)
