from django.db import models
from django.utils import timezone
from django.conf import settings

class Vaga(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    requisitos = models.TextField(blank=True)
    localizacao = models.CharField(max_length=255, blank=True)
    tipo_contrato = models.CharField(max_length=100, choices=[
        ('CLT', 'CLT'),
        ('PJ', 'Pessoa Jurídica'),
        ('Freelancer', 'Freelancer'),
        ('Estágio', 'Estágio'),
        ('Temporário', 'Temporário'),
    ])
    tipo_vaga = models.CharField(max_length=100, choices=[
        ('Presencial', 'Presencial'),
        ('Remoto', 'Remoto'),
        ('Híbrido', 'Híbrido'),
    ])
    publicada_em = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)
    empregador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titulo
