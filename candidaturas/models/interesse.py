from django.db import models
from django.conf import settings
from vagas.models.vaga import Vaga

class InteresseEmpregador(models.Model):
    empregador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    candidato = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avaliado_por')
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('curtido', 'Curtido'),
        ('dispensado', 'Dispensado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('empregador', 'candidato', 'vaga')

    def __str__(self):
        return f"{self.empregador.email} → {self.candidato.email} ({self.status})"
