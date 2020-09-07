from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators


class Currency(models.Model):
    CURRENCY_TYPES = (
        ('basic', 'BASIC'),
        ('secondary', 'SECONDARY')
    )

    name = models.CharField(max_length=10, blank=True)
    code = models.SmallIntegerField(default=1)
    short_name = models.CharField(max_length=3, blank=True, unique=True)
    symbol = models.CharField(max_length=1, blank=True)
    multiplicity = models.SmallIntegerField(default=1)
    currency_type = models.CharField(max_length=9, choices=CURRENCY_TYPES, default='SECONDARY')
    course = models.DecimalField(max_digits=8, decimal_places=4, blank=True, default=1)

    def __str__(self):
        return self.name


class AdvUser(AbstractUser):
    balance = models.DecimalField(max_digits=8, decimal_places=2, validators=[validators.MinValueValidator(0)])
    currency = models.ForeignKey(Currency, to_field='short_name', on_delete=models.PROTECT)
    username = models.EmailField(unique=True)
    password = models.CharField(max_length=256, validators=[validators.MinLengthValidator(8)])


class Transfers(models.Model):
    TRANSFER_TYPES = (
        ('income', 'INCOME'),
        ('outcome', 'OUTCOME')
    )

    COUNTERPARTY_TYPES = (
        ('sender', 'SENDER'),
        ('receiver', 'RECEIVER'),
    )

    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.SmallIntegerField()
    account = models.ForeignKey(AdvUser, on_delete=models.PROTECT,
                                related_name='original_account')
    transfer_type = models.CharField(max_length=7, choices=TRANSFER_TYPES, default='outcome')
    counterparty_account = models.ForeignKey(AdvUser, to_field='username', on_delete=models.PROTECT,
                                             default=1, related_name='counterparty_account')
    counterparty_type = models.CharField(max_length=7, choices=TRANSFER_TYPES, default='receiver')