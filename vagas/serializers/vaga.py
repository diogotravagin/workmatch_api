from rest_framework import serializers
from vagas.models.vaga import Vaga

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = '__all__'
        read_only_fields = ['empregador', 'publicada_em']
