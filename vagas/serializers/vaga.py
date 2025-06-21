from rest_framework import serializers
from vagas.models.vaga import Vaga

class VagaSerializer(serializers.ModelSerializer):
    nome_empresa = serializers.SerializerMethodField()

    class Meta:
        model = Vaga
        fields = '__all__'
        read_only_fields = ['empregador', 'publicada_em']

    def get_nome_empresa(self, obj):
        perfil = getattr(obj.empregador, "perfil_empregador", None)
        return perfil.empresa if perfil else "Empresa não informada"
