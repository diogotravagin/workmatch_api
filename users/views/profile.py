from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from users.serializers import UsuarioSerializer, CandidatoPerfilSerializer, EmpregadorPerfilSerializer
from users.models import CandidatoPerfil, EmpregadorPerfil

class UsuarioProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


class CandidatoPerfilView(generics.RetrieveAPIView):
    serializer_class = CandidatoPerfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return CandidatoPerfil.objects.get(usuario=self.request.user)
        except CandidatoPerfil.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        perfil = self.get_object()
        if not perfil:
            return Response(
                {"detail": "Perfil de candidato ainda não foi criado."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(perfil)
        return Response(serializer.data)


class EmpregadorPerfilView(generics.RetrieveUpdateAPIView):
    queryset = EmpregadorPerfil.objects.all()
    serializer_class = EmpregadorPerfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.queryset.get(usuario=self.request.user)
        except EmpregadorPerfil.DoesNotExist:
            raise NotFound("Perfil de empregador não encontrado")


class CriarCandidatoPerfilView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, 'perfil_candidato'):
            return Response(
                {"detail": "Perfil de candidato já existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CandidatoPerfilSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


