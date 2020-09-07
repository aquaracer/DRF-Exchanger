from rest_framework import serializers
from .models import Transfers, AdvUser


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfers
        fields = ('amount', 'counterparty_account')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvUser
        fields = ('username', 'password', 'balance', 'currency')
