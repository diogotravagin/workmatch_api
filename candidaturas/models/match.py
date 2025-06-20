from django.db import models
from django.conf import settings
from vagas.models.vaga import Vaga

class Match(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, null=True, blank=True)
    candidato = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='matches_como_candidato')
    empregador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='matches_como_empregador')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('vaga', 'candidato', 'empregador')

    def __str__(self):
        return f"Match: {self.candidato.email} ↔ {self.vaga.titulo}"
