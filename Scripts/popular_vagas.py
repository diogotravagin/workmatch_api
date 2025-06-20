import django
import os
import random
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workmatch_api.settings")
django.setup()

from vagas.models.vaga import Vaga
from users.models import Usuario

# 🔐 Dados do empregador já existente
EMAIL_EMPREGADOR = "empresa@teste.com"

def run():
    try:
        empregador = Usuario.objects.get(email=EMAIL_EMPREGADOR)
    except Usuario.DoesNotExist:
        print(f"❌ Empregador com e-mail '{EMAIL_EMPREGADOR}' não encontrado.")
        return

    print("🧹 Limpando todas as vagas...")
    Vaga.objects.all().delete()

    print("✅ Criando 10 vagas de teste...")
    contratos = ['CLT', 'PJ', 'Freelancer', 'Estágio', 'Temporário']
    tipos = ['Presencial', 'Remoto', 'Híbrido']

    for i in range(1, 11):
        vaga = Vaga.objects.create(
            titulo=f"Vaga Teste {i}",
            descricao=f"Descrição da vaga número {i}.",
            requisitos="Conhecimentos básicos exigidos.",
            localizacao="São Paulo - SP",
            tipo_contrato=random.choice(contratos),
            tipo_vaga=random.choice(tipos),
            publicada_em=timezone.now(),
            ativa=True,
            empregador=empregador
        )
        print(f"✔️ Criada: {vaga.titulo}")

    print("🏁 Finalizado com sucesso!")

if __name__ == "__main__":
    run()
