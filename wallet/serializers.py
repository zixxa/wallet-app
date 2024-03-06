from rest_framework import serializers
from wallet.models import Wallet


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('name', 'score', 'currency')