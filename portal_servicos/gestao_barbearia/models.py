from django.db import models
from portal.models import Barbearia, CustomUser


class Funcionario(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    barbearia = models.ForeignKey(Barbearia, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class Funcao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    duracao = models.DurationField()  # duração do serviço
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

 
class Agendamento(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agendamentos')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()

    class Meta:
        unique_together = ['funcionario', 'data_hora']

    def __str__(self):
        return f"{self.cliente.username} - {self.funcionario.user.username} - {self.data_hora}"

    
