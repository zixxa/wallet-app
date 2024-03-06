from decimal import Decimal

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from wallet.models import Wallet, Profile, convert_to_currency
from wallet.serializers import WalletTransactionSerializer


class WalletAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        wallets = Wallet.objects.filter(profile__user_id=request.user.id)

        content = {
            wallet.name: (
                convert_to_currency(wallet.score, wallet.currency.name),
                wallet.currency.name,
            )
            for wallet in wallets
        }
        return Response(content)

    def post(self, request):
        data = self.request.data
        score_by_rate = convert_to_currency(data["payment"], data["currency"])
        transaction_data = {
            "name": data["wallet_sender_name"],
            "score": round(score_by_rate, 2),
        }
        serializer = WalletTransactionSerializer(data=transaction_data)

        if serializer.is_valid():
            sender = Wallet.objects.get(
                profile__user_id=request.user.id, name=data["wallet_sender_name"]
            )
            payment = Decimal(data["payment"], 2)

            if payment > convert_to_currency(sender.score, data["currency"]):
                sender.create_error_transaction(
                    error_description="Недостаточно средств для перевода"
                )
                return Response(
                    "Недостаточно средств для перевода",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            receiver = Wallet.objects.get(name=data["wallet_receiver_name"])
            sender.create_transaction(
                payment=payment, currency=data["currency"], is_sender=True
            )
            receiver.create_transaction(
                payment=payment, currency=data["currency"], is_sender=False
            )
            content = {
                "user_sender": Profile.objects.get(
                    user_id=request.user.id
                ).user.username,
                "wallet_sender": sender.name,
                "wallet_receiver": receiver.name,
                "score_sender": sender.score,
            }
            return Response(content, status=status.HTTP_200_OK)
        return Response("Ошибка в запросе", status=status.HTTP_400_BAD_REQUEST)
