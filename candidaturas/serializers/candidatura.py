from rest_framework import serializers
from candidaturas.models import Candidatura
from vagas.serializers.vaga import VagaSerializer

class CandidaturaSerializer(serializers.ModelSerializer):
    vaga = VagaSerializer()

    class Meta:
        model = Candidatura
        fields = ['id', 'vaga', 'status', 'criada_em']
