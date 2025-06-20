from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.auth import UsuarioCreateView, UsuarioDetailView, CustomTokenObtainPairView
from .views.profile import UsuarioProfileView, CandidatoPerfilView, EmpregadorPerfilView, CriarCandidatoPerfilView

urlpatterns = [
    path('registrar/', UsuarioCreateView.as_view(), name='usuario-create'),
    path('perfil/', UsuarioDetailView.as_view(), name='usuario-detail'),
    path('perfil/candidato/', CandidatoPerfilView.as_view(), name='perfil-candidato'),
    path('perfil/candidato/criar/', CriarCandidatoPerfilView.as_view(), name='criar-perfil-candidato'),
    path('perfil/empregador/', EmpregadorPerfilView.as_view(), name='perfil-empregador'),
    path('me/', UsuarioProfileView.as_view(), name='usuario_profile'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

