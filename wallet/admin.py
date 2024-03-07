from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from wallet.models import Profile, Wallet, Transaction, Currency


class TransactionAdminInline(admin.TabularInline):
    model = Transaction
    readonly_fields = ("description",)


class WalletAdminInline(admin.TabularInline):
    model = Wallet


@register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("name",)
    inlines = (WalletAdminInline,)


@register(Wallet)
class WalletAdmin(ModelAdmin):
    inlines = (TransactionAdminInline,)


@register(Currency)
class CurrencyAdmin(ModelAdmin):
    list_display = ("name", "rate")
