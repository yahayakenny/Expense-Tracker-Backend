from django.urls import path

from . import views

app_name = "expense"

urlpatterns = [
    path("expense/", views.ExpenseListView.as_view(), name="expense"),
    path("expense/<int:pk>/", views.ExpenseDetailView.as_view(), name="expense"),
    path("expense/export-excel/", views.ExportExpenseExcel.as_view(), name="export_excel"),
    path("expense/export-csv/", views.ExportExpenseCsv.as_view(), name="export_csv"),
    path("expense/export-pdf/", views.ExportExpensePdf.as_view(), name="export_pdf"),
]
