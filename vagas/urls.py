from django.urls import path
from vagas.views.vaga import (
    CriarVagaView,
    ListarTodasVagasView,
    ListarMinhasVagasView,
    DetalharVagaView,
    VagasRecomendadasView
)

urlpatterns = [
    path('criar/', CriarVagaView.as_view(), name='criar-vaga'),
    path('', ListarTodasVagasView.as_view(), name='listar-vagas'),
    path('minhas/', ListarMinhasVagasView.as_view(), name='minhas-vagas'),
    path('<int:pk>/', DetalharVagaView.as_view(), name='detalhar-vaga'),
    path('recomendadas/', VagasRecomendadasView.as_view(), name='vagas-recomendadas')
]
