from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models




class Barbearia(models.Model):
    nome = models.CharField(max_length=100)
    tipo_assinatura = models.CharField(max_length=50)
    assinatura_ativa = models.BooleanField(default=True)
    aberto = models.BooleanField(default=True)
    owner_app = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='owned_barbearias')


    def __str__(self):
        return self.nome

class CustomUser(AbstractUser):
    is_owner_portal = models.BooleanField('Adm Portal', default=False)
    is_owner_app = models.BooleanField('Adm App', default=False)
    is_staff_portal = models.BooleanField('Func. Portal', default=False)
    is_staff_app = models.BooleanField('Func. App', default=False)
    is_client_portal = models.BooleanField('Cliente Portal', default=False)
    is_client_app = models.BooleanField('Cliente App', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    telefone = models.CharField('Telefone', max_length=12, blank=True, null=True)
    barbearias = models.ManyToManyField(Barbearia, related_name='clientes')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username



