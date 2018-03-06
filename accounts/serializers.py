from rest_framework import serializers

from accounts.models import JibambeUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = JibambeUser
        fields = ('phone_number', 'password', 'balance')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = JibambeUser
        fields = ('phone_number', 'password')
