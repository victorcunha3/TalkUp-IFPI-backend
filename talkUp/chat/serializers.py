from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Usuario, Perfil, Publicacao, Curtida, Comentario
from rest_framework.authentication import get_user_model
from rest_framework import serializers
from rest_framework.validators import ValidationError

class PerfilSerializer(ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['bio', 'data_nascimento']

Usuario = get_user_model()

class UsuarioSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'password')

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise ValidationError('Este email já está cadastrado')
        return value
    
    def create(self, validated_data):
        usuario = Usuario.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
            )
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario

class CurtidaSerializer(ModelSerializer):

    class Meta:
        model = Curtida
        fields = '__all__'

from datetime import datetime

class ComentarioSerializer(ModelSerializer):
    usuario = serializers.StringRelatedField(source='usuario.username')  # Exibir o nome do autor
    data_comentario_formatada = SerializerMethodField()
    #meta
    class Meta:
        model = Comentario
        fields = ['id', 'conteudo', 'data_comentario', 'usuario', 'publicacao', 'data_comentario_formatada']

    def get_data_comentario_formatada(self, comentario):
        data_comentario = comentario.data_comentario
        if data_comentario:
            return data_comentario.strftime('%Y-%m-%d')
        return None


class PublicacaoSerializer(ModelSerializer):
    comentarios = SerializerMethodField()
    autor = serializers.StringRelatedField(source='autor.username', read_only=True)
    data_publicacao_formatada = SerializerMethodField()

    class Meta:
        model = Publicacao
        fields = '__all__'
    
    def get_comentarios(self, publicacao):
        comentarios_relacionados = Comentario.objects.filter(publicacao=publicacao)
        comentarios_serializers = ComentarioSerializer(comentarios_relacionados, many=True)
        return comentarios_serializers.data

    def get_data_publicacao_formatada(self, publicacao):
        # Formate a data da publicação no formato desejado
        return datetime.strftime(publicacao.data_publicacao, '%Y-%m-%d')

    
