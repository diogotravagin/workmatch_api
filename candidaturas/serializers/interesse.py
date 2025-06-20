from rest_framework import serializers
from candidaturas.models.interesse import InteresseEmpregador
from users.serializers import UsuarioPublicoSerializer

class InteresseEmpregadorSerializer(serializers.ModelSerializer):
    candidato = UsuarioPublicoSerializer(read_only=True)

    class Meta:
        model = InteresseEmpregador
        fields = ['id', 'vaga', 'candidato', 'status', 'criado_em']
        read_only_fields = ['id', 'criado_em']
