import os
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, Client
from wallet.models import (
    Wallet,
    Profile,
    Currency,
    Transaction,
    DEFAULT_CURRENCY,
    convert_to_currency,
)


class TestWalletAPI(TestCase):
    wallet_1: Wallet
    wallet_2: Wallet
    wallet_3_1: Wallet
    wallet_3_2: Wallet
    user_1: User
    user_2: User
    user_3: User
    profile_1: Profile
    profile_1: Profile

    def setUp(self):
        self.user_data_1 = {
            "username": "joeuser",
            "profile_name": "billy",
            "password": "12345",
            "wallet_name": "id86531",
            "wallet_score": 300.00,
            "wallet_currency": "RUB",
        }
        self.user_data_2 = {
            "username": "ricky100",
            "profile_name": "michael",
            "password": "12345",
            "wallet_name": "id86532",
            "wallet_score": 300.00,
            "wallet_currency": "RUB",
        }

        self.user_data_3 = {
            "username": "bobby",
            "profile_name": "aaa",
            "password": "345",
            "wallet_name_1": "id86536",
            "wallet_score_1": 345.00,
            "wallet_currency_1": "RUB",
            "wallet_name_2": "id86538",
            "wallet_score_2": 200.00,
            "wallet_currency_2": "USD",
        }

        user_data_1 = self.user_data_1
        user_data_2 = self.user_data_2
        user_data_3 = self.user_data_3

        self.currency_rub = Currency.objects.create(name="RUB", rate=Decimal(1.000))
        self.currency_usd = Currency.objects.create(name="USD", rate=Decimal(0.011))
        self.currency_tst = Currency.objects.create(name="TST", rate=Decimal(1.278))

        self.user_1 = User.objects.create_user(
            username=user_data_1["username"], password=user_data_1["password"]
        )
        self.profile_1 = Profile.objects.create(
            user=self.user_1, name=user_data_1["profile_name"]
        )
        self.wallet_1 = Wallet.objects.create(
            name=user_data_1["wallet_name"],
            score=user_data_1["wallet_score"],
            profile=self.profile_1,
            currency=self.currency_rub,
        )

        self.user_2 = User.objects.create_user(
            username=user_data_2["username"], password=user_data_2["password"]
        )
        self.profile_2 = Profile.objects.create(
            user=self.user_2, name=user_data_2["profile_name"]
        )
        self.wallet_2 = Wallet.objects.create(
            name=user_data_2["wallet_name"],
            score=user_data_2["wallet_score"],
            profile=self.profile_2,
            currency=self.currency_rub,
        )

        self.user_3 = User.objects.create_user(
            username=user_data_3["username"], password=user_data_3["password"]
        )
        self.profile_3 = Profile.objects.create(
            user=self.user_3, name=user_data_3["profile_name"]
        )
        self.wallet_3_1 = Wallet.objects.create(
            name=user_data_3["wallet_name_1"],
            score=user_data_3["wallet_score_1"],
            profile=self.profile_3,
            currency=self.currency_rub,
        )
        self.wallet_3_2 = Wallet.objects.create(
            name=user_data_3["wallet_name_2"],
            score=user_data_3["wallet_score_2"],
            profile=self.profile_3,
            currency=self.currency_usd,
        )

        self.transaction = {
            "wallet_sender_name": "id86531",
            "wallet_receiver_name": "id86532",
            "payment": 50,
            "currency": "RUB",
        }

        self.transaction_in_usd_wallet = {
            "wallet_sender_name": "id86531",
            "wallet_receiver_name": "id86538",
            "payment": 50,
            "currency": "RUB",
        }

        self.balance_error_transaction = {
            "wallet_sender_name": "id86531",
            "wallet_receiver_name": "id86532",
            "payment": 350.00,
            "currency": "RUB",
        }
        self.payment_another_currency_transaction = {
            "wallet_sender_name": "id86531",
            "wallet_receiver_name": "id86532",
            "payment": 2.00,
            "currency": "USD",
        }
        self.client = Client()

    def test_post_transaction(self):
        self.client.login(username="joeuser", password="12345")
        response = self.client.post("/", data=self.transaction)
        self.assertEqual(response.status_code, 200)
        payment = self.transaction["payment"]
        sender_wallet = Wallet.objects.get(name=self.transaction["wallet_sender_name"])
        receiver_wallet = Wallet.objects.get(
            name=self.transaction["wallet_receiver_name"]
        )
        self.assertEqual(
            sender_wallet.score, self.user_data_1["wallet_score"] - payment
        )
        self.assertEqual(
            receiver_wallet.score, self.user_data_2["wallet_score"] + payment
        )
        transaction_1 = Transaction.objects.get(wallet=sender_wallet)
        transaction_2 = Transaction.objects.get(wallet=receiver_wallet)
        self.assertEqual(
            transaction_1.description,
            f"-{'{:.2f}'.format(payment)} {self.transaction['currency']} - Счет: {sender_wallet.score} {DEFAULT_CURRENCY}",
        )
        self.assertEqual(
            transaction_2.description,
            f"+{'{:.2f}'.format(payment)} {self.transaction['currency']} - Счет: {receiver_wallet.score} {DEFAULT_CURRENCY}",
        )

    def test_post_transaction_in_another_currency_wallet(self):
        self.client.login(username="joeuser", password="12345")

        transaction_data = self.transaction_in_usd_wallet
        response = self.client.post("/", data=self.transaction_in_usd_wallet)
        self.assertEqual(response.status_code, 200)
        payment = self.transaction_in_usd_wallet["payment"]
        converted_payment = convert_to_currency(payment, transaction_data["currency"])
        sender_wallet = Wallet.objects.get(name=transaction_data["wallet_sender_name"])
        receiver_wallet = Wallet.objects.get(
            name=transaction_data["wallet_receiver_name"]
        )
        self.assertEqual(
            sender_wallet.score,
            Decimal(str(self.user_data_1["wallet_score"])) - converted_payment,
        )
        self.assertEqual(
            receiver_wallet.score,
            Decimal(str(self.user_data_3["wallet_score_2"])) + converted_payment,
        )
        transaction_1 = Transaction.objects.get(wallet=sender_wallet)
        transaction_2 = Transaction.objects.get(wallet=receiver_wallet)
        self.assertEqual(
            transaction_1.description,
            f"-{'{:.2f}'.format(payment)} {transaction_data['currency']} - Счет: {str(convert_to_currency(sender_wallet.score, sender_wallet.currency.name))} {sender_wallet.currency.name}",
        )
        self.assertEqual(
            transaction_2.description,
            f"+{'{:.2f}'.format(payment)} {transaction_data['currency']} - Счет: {str(convert_to_currency(receiver_wallet.score, receiver_wallet.currency.name))} {receiver_wallet.currency.name}",
        )

    def test_post_payment_validate_another_currency(self):
        self.client.login(username="joeuser", password="12345")
        transaction_data = self.payment_another_currency_transaction
        response = self.client.post("/", data=transaction_data)
        self.assertEqual(response.status_code, 200)
        payment = transaction_data["payment"]
        sender_wallet = Wallet.objects.get(name=transaction_data["wallet_sender_name"])
        receiver_wallet = Wallet.objects.get(
            name=transaction_data["wallet_receiver_name"]
        )
        converted_payment = convert_to_currency(payment, transaction_data["currency"])
        self.assertEqual(
            sender_wallet.score,
            Decimal(str(self.user_data_1["wallet_score"])) - converted_payment,
        )
        self.assertEqual(
            receiver_wallet.score,
            Decimal(str(self.user_data_2["wallet_score"])) + converted_payment,
        )
        transaction_1 = Transaction.objects.get(wallet=sender_wallet)
        transaction_2 = Transaction.objects.get(wallet=receiver_wallet)
        self.assertEqual(
            transaction_1.description,
            f"-{'{:.2f}'.format(converted_payment)} {transaction_data['currency']} - Счет: {sender_wallet.score} {DEFAULT_CURRENCY}",
        )
        self.assertEqual(
            transaction_2.description,
            f"+{'{:.2f}'.format(converted_payment)} {transaction_data['currency']} - Счет: {receiver_wallet.score} {DEFAULT_CURRENCY}",
        )

    def test_post_payment_validate_balance_error(self):
        self.client.login(username="joeuser", password="12345")
        transaction_data = self.balance_error_transaction
        response = self.client.post("/", data=transaction_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "Недостаточно средств для перевода")
        sender_wallet = Wallet.objects.get(name=transaction_data["wallet_sender_name"])
        receiver_wallet = Wallet.objects.get(
            name=transaction_data["wallet_receiver_name"]
        )
        self.assertEqual(sender_wallet.score, self.user_data_1["wallet_score"])
        self.assertEqual(receiver_wallet.score, self.user_data_2["wallet_score"])
        transaction_1 = Transaction.objects.get(wallet=sender_wallet)
        self.assertEqual(
            transaction_1.description,
            'Транзакция завершилась ошибкой "Недостаточно средств для перевода" - Счет: 300.00 RUB',
        )

    def test_post_without_auth(self):
        response = self.client.post("/", data=self.transaction)
        self.assertEquals(response.status_code, 403)

    def test_get_many_wallets(self):
        user_data = {"name": "bobby", "password": "345"}
        wallets = Wallet.objects.filter(profile__user__username=user_data["name"])
        self.client.login(username=user_data["name"], password=user_data["password"])
        response = self.client.get("/")

        self.assertEqual(
            response.json(),
            {
                wallet.name: [
                    float(convert_to_currency(wallet.score, wallet.currency.name)),
                    wallet.currency.name,
                ]
                for wallet in wallets
            },
        )
