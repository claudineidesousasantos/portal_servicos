from django.contrib import admin
from .models import Cliente, CustomUser

class ClienteAdmin(admin.ModelAdmin):
    list_display = ['user', 'barbearia']
    search_fields = ['user__username', 'barbearia__nome']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(is_client_app=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Cliente, ClienteAdmin)
