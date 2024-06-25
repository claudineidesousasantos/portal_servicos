
from django import forms
from portal.models import CustomUser
from .models import Funcionario, Funcao, Agendamento


class FuncionarioForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_staff=True))

    class Meta:
        model = Funcionario
        fields = ['user', 'barbearia']
        
class FuncionarioCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    funcao = forms.ModelChoiceField(queryset=Funcao.objects.all())

    class Meta:
        model = Funcionario
        fields = ['barbearia', 'funcao']

    def save(self, commit=True):
        user_data = {
            'username': self.cleaned_data['username'],
            'password': self.cleaned_data['password'],
            'first_name': self.cleaned_data.get('first_name', ''),
            'last_name': self.cleaned_data.get('last_name', ''),
            'email': self.cleaned_data.get('email', ''),
        }
        user = CustomUser.objects.create_user(**user_data)
        funcionario = super().save(commit=False)
        funcionario.user = user
        if commit:
            funcionario.save()
        return funcionario


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['servico', 'data_hora']

    def __init__(self, *args, **kwargs):
        self.funcionario = kwargs.pop('funcionario', None)
        super().__init__(*args, **kwargs)
        if self.funcionario:
            self.fields['servico'].queryset = self.funcionario.barbearia.servicos.all()

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