# Generated by Django 5.0.3 on 2024-03-06 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_currency_rate_alter_wallet_score'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='currency',
            table='currency',
        ),
    ]