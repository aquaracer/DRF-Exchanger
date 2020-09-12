from rest_framework import serializers
from .models import Transfers, AdvUser


class AddTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfers
        fields = ('amount', 'counterparty_account')


class TransfersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfers
        fields = ("datetime", "amount", "currency", "transfer_type", "counterparty_type", "counterparty_account")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvUser
        fields = ('username', 'password', 'balance', 'currency')
