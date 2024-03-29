# Generated by Django 5.0.3 on 2024-03-06 09:57

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0008_alter_currency_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currency",
            name="rate",
            field=models.DecimalField(decimal_places=10, default=1, max_digits=12),
        ),
        migrations.AlterField(
            model_name="wallet",
            name="score",
            field=models.DecimalField(
                decimal_places=10,
                default=100,
                max_digits=12,
                validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
            ),
        ),
    ]
