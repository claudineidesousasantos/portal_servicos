from django import forms
from gestao_barbearia.models import Agendamento, Funcao, Servico

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['servico', 'data_hora']
        widgets = {
            'data_hora': forms.TextInput(attrs={'class': 'form-control datetimepicker-input', 'data-td-target': '#datetimepicker1'}),
        }

    def __init__(self, *args, **kwargs):
        self.funcionario = kwargs.pop('funcionario', None)
        super().__init__(*args, **kwargs)
        if self.funcionario:
            funcoes = Funcao.objects.filter(funcionario=self.funcionario)
            self.fields['servico'].queryset = Servico.objects.filter(funcao__in=funcoes)

    def clean_data_hora(self):
        data_hora = self.cleaned_data['data_hora']
        duracao = self.cleaned_data['servico'].duracao
        conflito = Agendamento.objects.filter(
            funcionario=self.funcionario,
            data_hora__lt=data_hora + duracao,
            data_hora__gte=data_hora
        ).exists()
        if conflito:
            raise forms.ValidationError("Horário indisponível para agendamento.")
        return data_hora
