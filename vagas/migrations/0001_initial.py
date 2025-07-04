# Generated by Django 5.2.3 on 2025-06-17 19:01

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Vaga",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=255)),
                ("descricao", models.TextField()),
                ("requisitos", models.TextField(blank=True)),
                ("localizacao", models.CharField(blank=True, max_length=255)),
                (
                    "tipo_contrato",
                    models.CharField(
                        choices=[
                            ("CLT", "CLT"),
                            ("PJ", "Pessoa Jurídica"),
                            ("Freelancer", "Freelancer"),
                            ("Estágio", "Estágio"),
                            ("Temporário", "Temporário"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "publicada_em",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("ativa", models.BooleanField(default=True)),
                (
                    "empregador",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
