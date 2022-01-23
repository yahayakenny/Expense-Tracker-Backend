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
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            category = Category.objects.filter(user=request.user)
            serializer = CategorySerializer(category, many=True)
            data = {"filtered": serializer.data}
            return Response(data, status=status.HTTP_200_OK)

        except:
            return Response(
                data={"message": "Unable to get categories"}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            data = request.data
            category = Category.objects.create(name=data["name"], user=request.user)
            serializer = CategorySerializer(category, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"message": "Unable to create category"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )


class CategoryDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        if request.user == category.user:
            try:
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(
                    data={"message": "Unable to get category detail"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data={"message": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def put(self, request, pk):
        category = self.get_object(pk)
        if request.user == category.user:
            try:
                serializer = CategorySerializer(category, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        data={"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST
                    )
            except:
                return Response(
                    data={"message": "Unable to update category"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data={"message": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def delete(self, request, pk):
        category = self.get_object(pk)
        if request.user == category.user:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404
