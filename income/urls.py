from django.urls import path
from . import views

app_name = 'income'

urlpatterns = [
    path('income/', views.IncomeListView.as_view()),
    path('income/<int:pk>/', views.IncomeDetailView.as_view()),
]
