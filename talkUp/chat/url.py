from django.urls import path
from .views import UsuarioView, PerfilView, SignupAPIView, PublicacaoView, ListaPublicacoesPublicas, CurtirPublicacaoAPIView, ComentarioApiView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatters = [
    path('usuarios/', UsuarioView.as_view(), name="usuarios"),
    path('perfil/', PerfilView.as_view(), name="perfil"),
    path('signup/', SignupAPIView.as_view(), name="signup"),
    path('token/', TokenObtainPairView.as_view(), name='tokenPairView'),
    path('publicacao/', PublicacaoView.as_view(), name='publicacao'),
    path('publicacao/<int:pk>/', PublicacaoView.as_view(), name='publicacao-detail'),
    path('lista-publicacao/', ListaPublicacoesPublicas.as_view(), name='lista-publicacao'),
    path('publicacao/<int:publicacao_id>/curtir/', CurtirPublicacaoAPIView.as_view(), name='curtir_publicacao'),
    path('comentario/<int:publicacao_id>/', ComentarioApiView.as_view(), name='comentario')
]