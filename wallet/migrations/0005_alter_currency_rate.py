# Generated by Django 5.0.3 on 2024-03-06 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0004_alter_currency_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currency",
            name="rate",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
    ]
