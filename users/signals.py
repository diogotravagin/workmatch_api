from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from users.models import CandidatoPerfil, EmpregadorPerfil


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_perfil_automaticamente(sender, instance, created, **kwargs):
    if created:
        if instance.tipo == 'candidato':
            CandidatoPerfil.objects.create(usuario=instance)
        elif instance.tipo == 'empregador':
            EmpregadorPerfil.objects.create(usuario=instance)
