from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from candidaturas.models.match import Match
from candidaturas.serializers.match import MatchSerializer

class MatchListView(ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.tipo == 'candidato':
            return Match.objects.filter(candidato=user).order_by('-criado_em')
        elif user.tipo == 'empregador':
            return Match.objects.filter(empregador=user).order_by('-criado_em')
        return Match.objects.none()
