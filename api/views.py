from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .models import Transfers, AdvUser
from .serializers import AddTransferSerializer, TransfersSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.db.transaction import atomic
from decimal import Decimal


class NewUser(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ((IsAdminUser,))


class ApiTransfer(APIView):
    permission_classes = ((IsAuthenticated,))

    def get(self, request):
        transfers = Transfers.objects.filter(account_id=request.user.id)
        serializer = TransfersSerializer(transfers, many=True)
        return Response(serializer.data)

    @atomic()
    def post(self, request):
        serializer = AddTransferSerializer(data=request.data)
        if serializer.is_valid():
            sender = AdvUser.objects.get(username=request.user.username)
            receiver = AdvUser.objects.get(username=request.data['counterparty_account'])
            if sender == receiver:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            amount = Decimal(request.data['amount'])
            new_balance = sender.balance - amount
            if new_balance < 0:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            sender.balance = new_balance
            sender.save()
            Transfers.objects.create(account=sender,
                                     amount=amount,
                                     counterparty_account=receiver,
                                     currency=sender.currency)
            sender_currency = sender.currency.currency_type
            receiver_currency = receiver.currency.currency_type
            if sender.currency_id == receiver.currency_id:
                receiver.balance += amount
            elif sender_currency == 'basic' and receiver_currency != 'basic':
                receiver.balance += amount * receiver.currency.course
            elif sender_currency != 'basic' and receiver_currency == 'basic':
                receiver.balance += amount / sender.currency.course
            elif sender.currency_id != receiver.currency_id and sender_currency != 'basic' and sender_currency != 'basic':
                receiver.balance += amount * receiver.currency.course / sender.currency.course
            receiver.save()
            Transfers.objects.create(account=receiver,
                                     amount=amount,
                                     transfer_type='income',
                                     counterparty_account=sender,
                                     counterparty_type='sender',
                                     currency=sender.currency)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
