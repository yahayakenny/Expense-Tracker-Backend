from rest_framework.serializers import ModelSerializer

from settings.models import Settings


class SettingsSerializer(ModelSerializer):
    class Meta: 
        model = Settings
        fields = ['currency', 'limit']
        depth = 2
