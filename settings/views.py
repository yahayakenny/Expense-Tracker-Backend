from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Settings
from .serializers import SettingsSerializer


class SettingsListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            results = Settings.objects.all().filter(user=request.user).order_by("-id")
            serializer = SettingsSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Unable to retrieve settings"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        try:
            data = request.data
            settings = Settings.objects.create(
                currency=data["currency"], limit=data["limit"], user=request.user
            )
            serializer = SettingsSerializer(settings, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"message": "Unable to add settings"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SettingsDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Settings.objects.get(pk=pk)
        except Settings.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        settings = self.get_object(pk)
        if request.user == settings.user:
            serializer = SettingsSerializer(settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404

    def put(self, request, pk):
        settings = self.get_object(pk)
        if request.user == settings.user:
            serializer = SettingsSerializer(settings, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404

    def delete(self, request, pk):
        settings = self.get_object(pk)
        if request.user == settings.user:
            settings.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404
