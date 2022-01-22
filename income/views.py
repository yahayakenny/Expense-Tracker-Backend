from core.constants import current_month
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from income.serializers import IncomeSerializer

from .models import Income


class IncomeListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            results = (
                Income.objects.all()
                .filter(user=request.user)
                .filter(date__month=str(current_month))
            )
            serializer = IncomeSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to retrieve income"}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            data = request.data
            income = Income.objects.create(
                name=data["name"],
                amount=data["amount"],
                description=data["description"],
                user=request.user,
            )
            serializer = IncomeSerializer(income, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"message": "Unable to add new income"}, status=status.HTTP_400_BAD_REQUEST
            )


class IncomeDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Income.objects.get(pk=pk)
        except Income.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        income = self.get_object(pk)
        if request.user == income.user:
            serializer = IncomeSerializer(income)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            raise Http404

    def put(self, request, pk):
        income = self.get_object(pk)
        if request.user == income.user:
            serializer = IncomeSerializer(income, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404

    def delete(self, request, pk):
        income = self.get_object(pk)
        if request.user == income.user:
            income.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404
