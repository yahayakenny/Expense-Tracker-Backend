from .serializers import SettingsSerializer
from .models import Settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

class SettingsListView(APIView):

    def get(self, request, format = None):
        results = Settings.objects.all().filter(user=request.user).order_by('-id')
        serializer = SettingsSerializer(results, many = True)
        return Response(serializer.data)

    def post(self, request):
        data=request.data
        print(data)
        settings = Settings.objects.create(
            currency = data['currency'],
            limit = data['limit'],
            user = request.user
        )
        serializer = SettingsSerializer(settings, many = False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SettingsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Settings.objects.get(pk=pk)
        except Settings.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        settings = self.get_object(pk)
        if request.user == settings.user:
            serializer = SettingsSerializer(settings)
            return Response(serializer.data)
        else:
            raise Http404

    def put(self, request, pk):
        settings = self.get_object(pk)
        if request.user == settings.user:
            serializer = SettingsSerializer(settings, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            raise Http404

    def delete(self, request, pk):
        settings = self.get_object(pk)
        if request.user == settings.user:
            settings.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404
