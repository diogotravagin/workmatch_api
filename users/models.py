from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Usuario(AbstractUser):
    # Tipos de perfis
    TIPO_CANDIDATO = 'candidato'
    TIPO_EMPREGADOR = 'empregador'

    TIPOS_USUARIO = [
        (TIPO_CANDIDATO, 'Candidato'),
        (TIPO_EMPREGADOR, 'Empregador'),
    ]

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_USUARIO,
        default=TIPO_CANDIDATO
    )

    nome_completo = models.CharField(max_length=150)
    data_nascimento = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='perfis/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"


class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    descricao = models.TextField(blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class CandidatoPerfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    experiencia = models.TextField(blank=True)
    pretensao_salarial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Candidato: {self.usuario.username}"


class EmpregadorPerfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_empregador")
    empresa = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, blank=True)
    setor = models.CharField(max_length=100, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Empregador: {self.usuario.username}"


class Vaga(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    localizacao = models.CharField(max_length=255, blank=True)
    requisitos = models.TextField(blank=True)
    tipo_contrato = models.CharField(max_length=100,
                                     choices=[('CLT', 'CLT'), ('PJ', 'PJ'), ('Freelancer', 'Freelancer')])
    criada_em = models.DateTimeField(auto_now_add=True)
    empregador = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                   related_name="vagas", blank=True, null=True)  # Apenas usuários tipo "empregador"

    def __str__(self):
        return f'Vaga: {self.titulo} - {self.empresa.nome}'