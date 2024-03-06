from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

DEFAULT_CURRENCY = "RUB"


class Currency(models.Model):
    name = models.CharField(
        max_length=5, default=DEFAULT_CURRENCY, blank=False, null=False
    )
    rate = models.DecimalField(
        decimal_places=4, max_digits=10, blank=False, default=1, null=False
    )

    class Meta:
        db_table = "currency"


class Profile(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "profile"


def convert_to_currency(score, currency=DEFAULT_CURRENCY):
    return round(Decimal(score) / Currency.objects.get(name=currency).rate, 2)



"""
Изменения счета кошелька должны проходить только через эти методы:
create_transaction - изменение счета и добавление записи в транзакцию
create_error_transaction - создание записи транзакции с ошибкой
"""


class Wallet(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    score = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=False,
        default=100,
        null=False,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False, blank=True
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=False, blank=True
    )

    def create_transaction(self, payment, currency=DEFAULT_CURRENCY, is_sender=True):
        payment = convert_to_currency(payment, currency)
        self.score = self.score - payment if is_sender else self.score + payment
        transaction = Transaction.objects.create(wallet=self)
        converted_score = convert_to_currency(self.score, self.currency.name)
        transaction.description = f'{"-" if is_sender else "+"}{payment} {currency} - Счет: {converted_score} {self.currency.name}'
        transaction.save()
        self.save()

    def create_error_transaction(self, error_description):
        transaction = Transaction.objects.create(wallet=self)
        converted_score = convert_to_currency(self.score, self.currency.name)

        transaction.description = f'Транзакция завершилась ошибкой "{error_description}" - Счет: {converted_score} {self.currency.name}'
        transaction.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "wallet"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False, blank=True)
    description = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        db_table = "transaction"
