from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from core.views import (
    QueryNetView,
    QueryDateRangeView,
    QueryCategoryView,
    QueryDayGraph,
    QueryMonthGraph,
    QueryMostRecentView,
    QueryWeekGraph,
)


class TestCoreUrls(APITestCase):
    def test_query_net_url_is_resolved(self):
        url = reverse("core:query_net")
        self.assertEquals(resolve(url).func.view_class, QueryNetView)

    def test_query_category_url_is_resolved(self):
        url = reverse("core:query_category")
        self.assertEquals(resolve(url).func.view_class, QueryCategoryView)

    def test_query_day_graph__url_is_resolved(self):
        url = reverse("core:query_day_graph")
        self.assertEquals(resolve(url).func.view_class, QueryDayGraph)

    def test_query_month_graph_url_is_resolved(self):
        url = reverse("core:query_month_graph")
        self.assertEquals(resolve(url).func.view_class, QueryMonthGraph)

    def test_query_week_graph_url_is_resolved(self):
        url = reverse("core:query_week_graph")
        self.assertEquals(resolve(url).func.view_class, QueryWeekGraph)

    def test_query_most_recent_view_url_is_resolved(self):
        url = reverse("core:query_most_recent_expenses")
        self.assertEquals(resolve(url).func.view_class, QueryMostRecentView)

    def test_query_date_range_url_is_resolved(self):
        url = reverse("core:query_date_range")
        self.assertEquals(resolve(url).func.view_class, QueryDateRangeView)
