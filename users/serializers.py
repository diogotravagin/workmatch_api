from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from django.utils.translation import gettext_lazy as _
from .models import Usuario, CandidatoPerfil, EmpregadorPerfil

Usuario = get_user_model()

class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'tipo']
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def validate_password(selfself, value):
        try:
            validate_password(value)
        except serializers.ValidationError as e:
            # Traduz as mensagens conhecidas
            translated_errors = []
            for message in e.messages:
                if "too short" in message:
                    translated_errors.append("A senha deve ter pelo menos 8 caracteres.")
                elif "too common" in message:
                    translated_errors.append("Evite usar senhas muito comuns.")
                elif "entirely numeric" in message:
                    translated_errors.append("A senha não pode conter apenas números.")
                else:
                    translated_errors.append(message)
            raise serializers.ValidationError(translated_errors)

        return value

    def create(self, validated_data):
        user = Usuario(
            username=validated_data['username'],
            email=validated_data['email'],
            tipo=validated_data['tipo']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'tipo', 'nome_completo', 'data_nascimento']


class UsuarioPublicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome_completo', 'email', 'bio', 'foto_perfil']


class CandidatoPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatoPerfil
        fields = ['id', 'usuario', 'bio', 'telefone', 'criado_em']
        read_only_fields = ['id', 'usuario', 'criado_em']


class EmpregadorPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpregadorPerfil
        fields = ['id', 'usuario', 'empresa', 'cargo', 'telefone', 'criado_em']
        read_only_fields = ['id', 'usuario', 'criado_em']