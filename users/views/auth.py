from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from users.serializers import UsuarioCreateSerializer, UsuarioSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

Usuario = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        data.update({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'tipo': user.tipo,
                'nome_completo': user.nome_completo,
                'data_nascimento': user.data_nascimento,
            }
        })

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UsuarioCreateView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        usuario = serializer.save()

        if usuario.tipo == 'empregador':
            from users.models import EmpregadorPerfil
            EmpregadorPerfil.objects.create(usuario=usuario)
        elif usuario.tipo == 'candidato':
            from users.models import CandidatoPerfil
            CandidatoPerfil.objects.create(usuario=usuario)


class UsuarioDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)