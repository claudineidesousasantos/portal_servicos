from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from portal.models import Barbearia
from .models import Funcionario, Agendamento, Servico, Funcao
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return render(request, 'registration/login.html')

@login_required
def index(request):
    print("aqui 1")
    if request.user.is_owner_app:
        try:
            barbearia = Barbearia.objects.get(owner_app=request.user)
            funcionarios = Funcionario.objects.filter(barbearia=barbearia)
            for funcionario in funcionarios:
                funcoes = Funcao.objects.filter(funcionario=funcionario)
                for funcao in funcoes:
                    funcao.servicos = Servico.objects.filter(funcao=funcao)
                funcionario.funcoes = funcoes
        except Barbearia.DoesNotExist:
            barbearia = None
            funcionarios = []
        return render(request, 'gestao_barbearia/index.html', {'barbearia': barbearia, 'funcionarios': funcionarios, 'funcoes': funcoes})
    else:
        return render(request, 'gestao_barbearia/access_denied.html')


@login_required
def visualizar_agenda(request, funcionario_id):
    funcionario = get_object_or_404(Funcionario, id=funcionario_id)
    return render(request, 'gestao_barbearia/visualizar_agenda.html', {'funcionario': funcionario})

@login_required
def acessar_cliente_app(request, barbearia_id):
    barbearia = get_object_or_404(Barbearia, id=barbearia_id)
    if request.user.is_client_app and request.user.barbearias.filter(id=barbearia.id).exists():
        return redirect('cliente_barbearia:index')
    else:
        return redirect('cliente_barbearia:index')  # Redireciona diretamente para a página do cliente

@login_required
def visualizar_agenda(request, funcionario_id):
    funcionario = get_object_or_404(Funcionario, id=funcionario_id)
    agendamentos = funcionario.agendamentos.all().order_by('data_hora')
    return render(request, 'gestao_barbearia/visualizar_agenda.html', {'funcionario': funcionario, 'agendamentos': agendamentos})