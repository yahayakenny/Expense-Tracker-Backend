from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("query-date-range/", views.QueryDateRangeView.as_view(), name="query_date_range"),
    path("query-category/", views.QueryCategoryView.as_view(), name="query_category"),
    path("query-day-graph/", views.QueryDayGraph.as_view(), name="query_day_graph"),
    path("query-week-graph/", views.QueryWeekGraph.as_view(), name="query_week_graph"),
    path("query-month-graph/", views.QueryMonthGraph.as_view(), name="query_month_graph"),
    path(
        "query-most-recent-expenses/",
        views.QueryMostRecentView.as_view(),
        name="query_most_recent_expenses",
    ),
    path("query-net/", views.QueryNetView.as_view(), name="query_net"),
]
