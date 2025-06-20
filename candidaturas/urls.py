from django.urls import path
from candidaturas.views.candidatura import CandidatarVagaView, DispensarVagaView
from candidaturas.views.candidatura import MinhasCandidaturasView
from candidaturas.views.interesse import RecomendacaoCandidatosView
from candidaturas.views.interesse import SwipeCandidatoView
from candidaturas.views.match import MatchListView

urlpatterns = [
    path('vagas/<int:vaga_id>/candidatar/', CandidatarVagaView.as_view(), name='candidatar-vaga'),
    path('vagas/<int:vaga_id>/dispensar/', DispensarVagaView.as_view(), name='dispensar-vaga'),
    path('minhas-candidaturas/', MinhasCandidaturasView.as_view(), name='minhas-candidaturas'),
    path('vagas/<int:vaga_id>/recomendados/', RecomendacaoCandidatosView.as_view(), name='candidatos-recomendados'),
    path('vagas/<int:vaga_id>/avaliar/<int:candidato_id>/', SwipeCandidatoView.as_view(), name='avaliar-candidato'),
    path('matches/', MatchListView.as_view(), name='lista-matches'),
]