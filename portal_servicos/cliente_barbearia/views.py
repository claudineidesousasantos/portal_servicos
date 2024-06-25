from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from portal.models import CustomUser
from django.contrib import messages
from gestao_barbearia.models import Funcionario
from .models import Cliente
from .forms import AgendamentoForm

@login_required
def agendar(request, funcionario_id):
    funcionario = get_object_or_404(Funcionario, id=funcionario_id)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, funcionario=funcionario)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.cliente = request.user
            agendamento.funcionario = funcionario
            agendamento.duracao = form.cleaned_data['servico'].duracao
            agendamento.save()
            messages.success(request, 'Agendamento concluído com sucesso!')
            return redirect('cliente_barbearia:index')
    else:
        form = AgendamentoForm(funcionario=funcionario)
    return render(request, 'cliente_barbearia/agendar.html', {'form': form, 'funcionario': funcionario})

@login_required
def index(request):
    usuario = request.user
    barbearia = None
    funcionarios = []
    if usuario.is_client_app:
        try:
            cliente = Cliente.objects.get(user=usuario)
            barbearia = cliente.barbearia
            funcionarios = Funcionario.objects.filter(barbearia=barbearia)
        except Cliente.DoesNotExist:
            barbearia = None
    return render(request, 'cliente_barbearia/index.html', {'usuario': usuario, 'barbearia': barbearia, 'funcionarios': funcionarios})

