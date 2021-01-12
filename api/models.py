from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators


class Currency(models.Model):
    CURRENCY_TYPES = (
        ('basic', 'BASIC'),
        ('secondary', 'SECONDARY')
    )

    name = models.CharField("Название валюты", max_length=10)
    code = models.SmallIntegerField("Код валюты")
    short_name = models.CharField("Краткое название валюты", max_length=3, unique=True)
    symbol = models.CharField("Символ валюты", max_length=1)
    multiplicity = models.SmallIntegerField()
    currency_type = models.CharField("Тип валюты", max_length=9, choices=CURRENCY_TYPES, default='SECONDARY')
    course = models.DecimalField("Курс валюты", max_digits=8, decimal_places=4)

    def __str__(self):
        return self.name


class AdvUser(AbstractUser):
    balance = models.DecimalField("Баланс", max_digits=8, decimal_places=2,
                                  validators=[validators.MinValueValidator(0)])
    currency = models.ForeignKey(Currency, verbose_name="Валюта", to_field='short_name', on_delete=models.PROTECT)
    username = models.EmailField("Имя пользователя", unique=True)
    password = models.CharField("Пароль", max_length=256, validators=[validators.MinLengthValidator(8)])


class Transfers(models.Model):
    TRANSFER_TYPES = (
        ('income', 'INCOME'),
        ('outcome', 'OUTCOME')
    )

    COUNTERPARTY_TYPES = (
        ('sender', 'SENDER'),
        ('receiver', 'RECEIVER'),
    )

    datetime = models.DateTimeField("Дата и время перевода", auto_now_add=True)
    amount = models.DecimalField("Сумма перевода", max_digits=8, decimal_places=2,
                                 validators=[validators.MinValueValidator(0), validators.DecimalValidator(8, 2)])
    account = models.ForeignKey(AdvUser, on_delete=models.PROTECT, verbose_name="Счет", related_name='original_account')
    transfer_type = models.CharField("Тип перевода", max_length=7, choices=TRANSFER_TYPES, default='outcome')
    counterparty_account = models.ForeignKey(AdvUser, verbose_name="Счет контрагента", to_field='username',
                                             on_delete=models.PROTECT, related_name='counterparty_account')
    counterparty_type = models.CharField("Статус контрагента", max_length=7, choices=TRANSFER_TYPES, default='receiver')
    currency = models.ForeignKey(Currency, verbose_name="Валюта", to_field='short_name', on_delete=models.PROTECT,
                                 default='USD')
