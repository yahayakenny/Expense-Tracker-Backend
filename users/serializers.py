from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','name', 'username', 'email', 'isAdmin']

    def get_name(self, obj):
        name = f'{obj.first_name} {obj.last_name}'
        if name == '':
            name = obj.email
        return name

    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = ['id',
        'name',
        'username', 
        'email', 
        'isAdmin', 
        'token'
        ]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
        