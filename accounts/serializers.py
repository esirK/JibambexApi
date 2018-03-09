from rest_framework import serializers

from accounts.models import JibambeUser, JibambePayment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = JibambeUser
        fields = ('phone_number', 'password', 'balance', 'previous_balance', "online_balance")


class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JibambePayment
        fields = ('sender_phone', 'first_name', 'last_name', 'amount',
                  'transaction_reference', 'transaction_timestamp')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = JibambeUser
        fields = ('phone_number', 'password')


class LoggedInUser(serializers.ModelSerializer):
    class Meta:
        model = JibambeUser
        fields = ('phone_number', 'balance')
