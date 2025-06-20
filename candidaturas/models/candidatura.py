from django.db import models
from django.conf import settings
from vagas.models.vaga import Vaga


class Candidatura(models.Model):
    candidato = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name="candidaturas", blank=True, null=True)

    STATUS_CHOICES = [
        ('curtida', 'Curtida'),
        ('dispensada', 'Dispensada'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    criada_em = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('candidato', 'vaga')
