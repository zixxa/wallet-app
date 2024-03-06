# Generated by Django 5.0.3 on 2024-03-06 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0006_alter_wallet_score_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='rate',
            field=models.DecimalField(decimal_places=10, default=1, max_digits=10),
        ),
    ]