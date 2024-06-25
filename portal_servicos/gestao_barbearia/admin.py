from django.contrib import admin
from .models import Funcao, Funcionario, Servico, Agendamento
from portal.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django import forms
from .forms import FuncionarioForm

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class FuncionarioAdmin(admin.ModelAdmin):
    form = FuncionarioForm
    list_display = ['user', 'barbearia']
    search_fields = ['user__username', 'barbearia__nome']



    def save_model(self, request, obj, form, change):
        form.instance = obj
        return super().save_model(request, obj, form, change)
    
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']


admin.site.register(Funcao, FuncaoAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Servico)
admin.site.register(Agendamento)
