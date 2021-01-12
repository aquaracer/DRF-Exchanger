from decimal import Decimal
from rest_framework import status

from api.models import AdvUser, Transfers


def TransferFunds(sender_data, receiver_data):
    sender = AdvUser.objects.get(username=sender_data)
    receiver = AdvUser.objects.get(username=receiver_data['counterparty_account'])
    if sender == receiver:
        return status.HTTP_400_BAD_REQUEST
    amount = Decimal(receiver_data['amount'])
    new_balance = sender.balance - amount
    if new_balance < 0:
        return status.HTTP_400_BAD_REQUEST
    sender.balance = new_balance
    sender.save()
    Transfers.objects.create(account=sender, amount=amount, counterparty_account=receiver, currency=sender.currency)
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
    Transfers.objects.create(account=receiver, amount=amount, transfer_type='income', counterparty_account=sender,
                             counterparty_type='sender', currency=sender.currency)
    return status.HTTP_201_CREATED
