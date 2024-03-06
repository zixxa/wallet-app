# Generated by Django 5.0.3 on 2024-03-05 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="RUB", max_length=5)),
            ],
        ),
        migrations.RenameField(
            model_name="wallet",
            old_name="currency",
            new_name="score",
        ),
    ]
