from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from vagas.models.vaga import Vaga
from vagas.serializers.vaga import VagaSerializer
from rest_framework.response import Response
from users.models import CandidatoPerfil
from candidaturas.models import Candidatura
from rest_framework.views import APIView


class CriarVagaView(generics.CreateAPIView):
    serializer_class = VagaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        usuario = self.request.user

        print(f'usuario: {usuario.tipo}')

        if usuario.tipo=="empregador":
            serializer.save(empregador=usuario)
        else:
            raise PermissionDenied("Apenas empregadores podem criar vagas.")

class ListarTodasVagasView(generics.ListAPIView):
    queryset = Vaga.objects.filter(ativa=True).order_by('-publicada_em')
    serializer_class = VagaSerializer
    permission_classes = [permissions.AllowAny]


class ListarMinhasVagasView(generics.ListAPIView):
    serializer_class = VagaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vaga.objects.filter(empregador=self.request.user).order_by('-publicada_em')


class DetalharVagaView(generics.RetrieveAPIView):
    queryset = Vaga.objects.all()
    serializer_class = VagaSerializer
    permission_classes = [permissions.AllowAny]

class VagasRecomendadasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.tipo != 'candidato':
            return Response({"detail": "Apenas candidatos podem ver vagas recomendadas."}, status=403)

        try:
            perfil = CandidatoPerfil.objects.get(usuario=user)
        except CandidatoPerfil.DoesNotExist:
            return Response({"detail": "Perfil de candidato não encontrado."}, status=404)

        # Lógica simples de recomendação (exemplo: todas as vagas por enquanto)
        vagas = (Vaga.objects.filter(ativa=True).order_by('-publicada_em'))
        serializer = VagaSerializer(vagas, many=True)
        return Response(serializer.data)

class VagasDisponiveisParaCandidatoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user

        # Filtra vagas ativas que ainda não foram candidatas nem dispensadas
        vagas_visualizadas = Candidatura.objects.filter(candidato=usuario).values_list('vaga_id', flat=True)
        vagas = Vaga.objects.filter(ativa=True).exclude(id__in=vagas_visualizadas)

        serializer = VagaSerializer(vagas, many=True, context={'request': request})
        return Response(serializer.data)