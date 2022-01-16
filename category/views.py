from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .models import Category
from .serializers import CategorySerializer


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        category = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(category, many=True)
        data = {"filtered": serializer.data}
        return Response(data)

    def post(self, request):
        data = request.data
        category = Category.objects.create(name=data["name"], user=request.user)
        serializer = CategorySerializer(category, many=False)
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
