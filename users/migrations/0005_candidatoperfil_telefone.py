# Generated by Django 5.2.3 on 2025-06-17 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_remove_empregadorperfil_cargo_candidatoperfil_cidade_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidatoperfil",
            name="telefone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
