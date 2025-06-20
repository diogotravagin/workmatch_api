from rest_framework.generics import ListAPIView
from candidaturas.serializers.candidatura import CandidaturaSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from vagas.models.vaga import Vaga
from candidaturas.models import Candidatura, Match, InteresseEmpregador

class CandidatarVagaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, vaga_id):
        try:
            vaga = Vaga.objects.get(id=vaga_id)
        except Vaga.DoesNotExist:
            raise NotFound("Vaga não encontrada.")

        if Candidatura.objects.filter(candidato=request.user, vaga=vaga).exists():
            raise ValidationError("Você já interagiu com esta vaga.")

        # Registra a candidatura
        Candidatura.objects.create(
            candidato=request.user,
            vaga=vaga,
            status='curtida'
        )

        # Verifica se o empregador já curtiu esse candidato para a mesma vaga
        empregador_curtiu = InteresseEmpregador.objects.filter(
            vaga=vaga,
            candidato=request.user,
            status='curtido'
        ).exists()

        if empregador_curtiu:
            Match.objects.get_or_create(
                vaga=vaga,
                candidato=request.user,
                empregador=vaga.empregador
            )

        return Response({"detail": "Candidatura registrada com sucesso."}, status=status.HTTP_201_CREATED)


class DispensarVagaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, vaga_id):
        try:
            vaga = Vaga.objects.get(id=vaga_id)
        except Vaga.DoesNotExist:
            raise NotFound("Vaga não encontrada.")

        if Candidatura.objects.filter(candidato=request.user, vaga=vaga).exists():
            raise ValidationError("Você já interagiu com esta vaga.")

        Candidatura.objects.create(
            candidato=request.user,
            vaga=vaga,
            status='dispensada'
        )
        return Response({"detail": "Dispensa registrada com sucesso."}, status=status.HTTP_201_CREATED)


class MinhasCandidaturasView(ListAPIView):
    serializer_class = CandidaturaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Candidatura.objects.filter(
            candidato=self.request.user,
            status='curtida'
        ).order_by('-criada_em')