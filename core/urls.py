from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('query-date-range/', views.QueryDateRangeView.as_view()),
    path('query-category/', views.QueryCategoryView.as_view()),
    path('query-day-graph/', views.QueryDayGraph.as_view()),
    path('query-week-graph/', views.QueryWeekGraph.as_view()),
    path('query-month-graph/', views.QueryMonthGraph.as_view()),
    path('query-most-recent-expenses/', views.QueryMostRecentView.as_view()),
    path('query-net/', views.QueryNetView.as_view())
]
