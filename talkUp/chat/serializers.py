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

class ComentarioSerializer(ModelSerializer):
    
    class Meta:
        model = Comentario
        #fields = '__all__'
        fields = ['conteudo']

class PublicacaoSerializer(ModelSerializer):
    comentarios = SerializerMethodField()

    class Meta:
        model = Publicacao
        fields = '__all__'

def get_comentarios(self, publicacao):
        comentarios_relacionados = Comentario.objects.filter(publicacao=publicacao)
        comentarios_serializers = ComentarioSerializer(comentarios_relacionados, many=True)
        return comentarios_serializers.data