from rest_framework.pagination import PageNumberPagination
from expense.serializers import ExpenseSerializer, CategorySerializer
from .models import Category, Expense
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

class ExpenseListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        results = Expense.objects.filter(user=request.user).order_by('-id')
        serializer = ExpenseSerializer(results, many = True)
        return Response(serializer.data)

    def post(self, request):
        data=request.data
        expense = Expense.objects.create(
            name = data['name'],
            amount = data['amount'],
            description = data['description'],
            category_id = data['category'],
            user = request.user
        )
        serializer = ExpenseSerializer(expense, many = False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        expense = self.get_object(pk)
        if request.user == expense.user:
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data)
        else:
            raise Http404

    def put(self, request, pk):
        expense = self.get_object(pk)
        data=request.data
        if request.user == expense.user:
            expense.name = data['name']
            expense.amount = data ['amount']
            expense.description = data['description']
            expense.category_id = data['category']
            serializer = ExpenseSerializer(expense, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                raise Http404

    def delete(self, request, pk):
        expense = self.get_object(pk)
        if request.user == expense.user:
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404

class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        category = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(category, many = True)
        data = {"filtered": serializer.data}
        return Response(data)

    def post(self, request):
        data=request.data
        category = Category.objects.create(
            name = data['name'],
            user = request.user
        )
        serializer = CategorySerializer(category, many = False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        if request.user == category.user:
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        else:
            raise Http404

    def put(self, request, pk):
        category = self.get_object(pk)
        if request.user == category.user:
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404

    def delete(self, request, pk):
        category = self.get_object(pk)
        if request.user == category.user:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404
