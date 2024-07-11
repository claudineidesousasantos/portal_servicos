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
        # Converte a duração de timedelta para horas, minutos e segundos
        total_seconds = int(self.duracao.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Formata a duração como HH:MM:SS
        if hours == 0:
            duracao_formatada = f"{minutes:2}min"
        else:
            duracao_formatada = f"{hours:2}h {minutes:2}min"
        
        # Retorna o formato desejado
        return f"{self.nome} - {duracao_formatada}"

 
class Agendamento(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agendamentos')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='servicos')
    data_hora = models.DateTimeField()

    class Meta:
        unique_together = ['funcionario', 'data_hora']

    def __str__(self):
        # Formata a data e hora para o formato desejado
        data_hora_formatada = self.data_hora.strftime('%d/%m/%Y %H:%M')
        return f"Cliente {self.cliente.username} - Barbeiro {self.funcionario.user.username} - agendado para {data_hora_formatada}"

    
