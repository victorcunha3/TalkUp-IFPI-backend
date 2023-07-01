from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Usuario, Perfil, Publicacao, Comentario
from .serializers import UsuarioSerializer, PerfilSerializer, PublicacaoSerializer, ComentarioSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


class UsuarioView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PerfilView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        perfil = Perfil.objects.filter(usuario=request.user)
        serializer = PerfilSerializer(perfil, many=True)
        return Response(serializer.data)
    
    def put(self, request, pk=None):
        perfil = self.get_object(pk)
        serializer = PerfilSerializer(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        perfil = self.get_object(pk)
        perfil.bio = ''
        perfil.data_nascimento = None 
        perfil.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def get_object(self, pk):
        usuario = self.request.user
        try:
            return Perfil.objects.get(usuario=usuario)
        except Perfil.DoesNotExist:
            raise NotFound("Perfil não encontrado.")

class PublicacaoView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PublicacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(autor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        publicacao = Publicacao.objects.filter(autor=request.user)
        serializer = PublicacaoSerializer(publicacao, many=True)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        try:
            publicacao = Publicacao.objects.get(pk=pk, autor=request.user)
            publicacao.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Publicacao.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"erro": "Publicação não encontrada"})

class SignupAPIView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(data={"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListaPublicacoesPublicas(APIView):
    def get(self, request, format=None):
        publicacoes = Publicacao.objects.filter(visibilidade='publico')
        serializer = PublicacaoSerializer(publicacoes, many=True)
        return Response(serializer.data)


class CurtirPublicacaoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, publicacao_id):
        publicacao = get_object_or_404(Publicacao, id=publicacao_id)
        if publicacao.visibilidade != 'publico':
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if request.user in publicacao.curtidas.all():
            publicacao.curtidas.remove(request.user)
        else:
            publicacao.curtidas.add(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ComentarioApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, publicacao_id):
        try:
            publicacao = Publicacao.objects.get(id=publicacao_id, visibilidade='publico')
        except Publicacao.DoesNotExist:
            return Response({'erro': 'A publicação não existe ou não é pública.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            comentario = serializer.save(usuario=request.user, publicacao=publicacao)
            print(ComentarioSerializer(comentario).data)
            return Response(ComentarioSerializer(comentario).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #new    
    def get(self, request, publicacao_id):
        try:
            publicacao = Publicacao.objects.get(id=publicacao_id)
        except Publicacao.DoesNotExist:
            return Response({'erro': 'A publicação não existe.'}, status=status.HTTP_404_NOT_FOUND)

        comentarios = Comentario.objects.filter(publicacao=publicacao)
        serializer = ComentarioSerializer(comentarios, many=True)
        return Response(serializer.data)
    
