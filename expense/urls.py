from django.urls import path

from . import views

app_name = 'expense'

urlpatterns = [
    path('expense/', views.ExpenseListView.as_view()),
    path('expense/<int:pk>/', views.ExpenseDetailView.as_view()),
    path('expense/export-excel/', views.ExportExpenseExcel.as_view()),
    path('expense/export-csv/', views.ExportExpenseCsv.as_view()),
    path('expense/export-pdf/', views.ExportExpensePdf.as_view()),
    path('category/', views.CategoryListView.as_view()),
    path('category/<int:pk>/', views.CategoryDetailView.as_view()),
]
