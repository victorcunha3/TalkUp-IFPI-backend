from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

Usuario = get_user_model()

VISIBILIDADE_CHOICES = (
    ('publico', 'Público'),
    ('privado', 'Privado'),
)

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, related_name='perfil', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    data_nascimento = models.DateField(blank=True, null=True)

@receiver(post_save, sender=Usuario)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

class Publicacao(models.Model):
    autor = models.ForeignKey(Usuario, related_name='publicacoes', on_delete=models.CASCADE, blank=True)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    curtidas = models.ManyToManyField(Usuario, related_name='publicacoes_curtidas', blank=True)
    visibilidade = models.CharField(max_length=15, choices=VISIBILIDADE_CHOICES, default='publico')
    comentarios = models.ManyToManyField('Comentario', related_name='publicacoes', blank=True)

    def __str__(self) -> str:
        return self.autor.username
    
class Curtida(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='curtidas', on_delete=models.CASCADE)
    publicacao = models.ForeignKey(Publicacao, related_name='curtidas_relacionadas', on_delete=models.CASCADE)
    data_curtida = models.DateTimeField(default=timezone.now)

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='comentarios', on_delete=models.CASCADE, blank=True)
    publicacao = models.ForeignKey(Publicacao, related_name='comentario', on_delete=models.CASCADE, blank=True)
    conteudo = models.TextField()
    data_comentario = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.autor.username
