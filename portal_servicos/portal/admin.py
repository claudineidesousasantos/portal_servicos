from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Barbearia
from cliente_barbearia.models import Cliente


class CustomUserAdmin(UserAdmin):
    list_editable = ['telefone', 'is_owner_portal', 'is_owner_app']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('telefone', 'is_owner_portal', 'is_owner_app', 'is_staff_portal', 'is_staff_app', 'is_client_portal', 'is_client_app', 'barbearias')}),
    )
    list_display = ['username', 'email', 'telefone', 'is_owner_portal', 'is_owner_app', 'is_client_app', 'get_owned_apps', 'get_client_barbearia']
    
    def get_owned_apps(self, obj):
        apps = obj.owned_barbearias.all()
        return ", ".join([app.nome for app in apps])
    get_owned_apps.short_description = 'Owned Apps'
    
    def get_client_barbearia(self, obj):
        if obj.is_client_app:
            try:
                cliente = Cliente.objects.get(user=obj)
                return cliente.barbearia.nome
            except Cliente.DoesNotExist:
                return 'Nenhuma'
        return '-'
    get_client_barbearia.short_description = 'Barbearia Associada'

admin.site.register(CustomUser, CustomUserAdmin)

class BarbeariaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_assinatura', 'assinatura_ativa', 'aberto', 'owner_app']
    search_fields = ['nome', 'tipo_assinatura', 'owner_app__username']
    ordering = ['nome']

admin.site.register(Barbearia, BarbeariaAdmin)
