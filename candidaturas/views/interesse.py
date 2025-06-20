from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from users.models import Usuario
from users.serializers import UsuarioPublicoSerializer
from candidaturas.models.interesse import InteresseEmpregador
from candidaturas.models.candidatura import Candidatura
from candidaturas.models.match import Match
from vagas.models.vaga import Vaga


class SwipeCandidatoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, vaga_id, candidato_id):
        vaga = Vaga.objects.filter(id=vaga_id, empregador=request.user).first()
        if not vaga:
            raise NotFound("Vaga não encontrada ou não pertence a você.")

        candidato = Usuario.objects.filter(id=candidato_id, tipo='candidato').first()
        if not candidato:
            raise NotFound("Candidato não encontrado.")

        if InteresseEmpregador.objects.filter(empregador=request.user, vaga=vaga, candidato=candidato).exists():
            raise ValidationError("Você já avaliou esse candidato para esta vaga.")

        status_swipe = request.data.get('status')
        if status_swipe not in ['curtido', 'dispensado']:
            raise ValidationError("Status inválido. Use 'curtido' ou 'dispensado'.")

        # Registra a interação
        InteresseEmpregador.objects.create(
            empregador=request.user,
            candidato=candidato,
            vaga=vaga,
            status=status_swipe
        )

        # Se for curtido, verificar se o candidato também curtiu a vaga
        if status_swipe == 'curtido':
            candidato_curtou = Candidatura.objects.filter(
                candidato=candidato,
                vaga=vaga,
                status='curtida'
            ).exists()

            if candidato_curtou:
                Match.objects.get_or_create(
                    vaga=vaga,
                    candidato=candidato,
                    empregador=request.user
                )

        return Response({"detail": "Interação registrada com sucesso."}, status=status.HTTP_201_CREATED)


class RecomendacaoCandidatosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vaga_id):
        vaga = Vaga.objects.filter(id=vaga_id, empregador=request.user).first()
        if not vaga:
            raise NotFound("Vaga não encontrada ou não pertence a você.")

        # IDs de candidatos já avaliados
        candidatos_avaliados = InteresseEmpregador.objects.filter(
            vaga=vaga,
            empregador=request.user
        ).values_list('candidato_id', flat=True)

        # Buscar candidatos ainda não avaliados
        candidatos_disponiveis = Usuario.objects.filter(
            tipo='candidato'
        ).exclude(id__in=candidatos_avaliados)

        # Se quiser retornar apenas um para swipe:
        candidato = candidatos_disponiveis.first()
        if not candidato:
            return Response({"detail": "Não há mais candidatos recomendados."})

        # Simula uma recomendação: retorna o próximo não avaliado
        serializer = UsuarioPublicoSerializer(candidato)
        return Response(serializer.data)