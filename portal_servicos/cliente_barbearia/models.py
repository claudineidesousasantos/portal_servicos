from django.db import models
from portal.models import CustomUser, Barbearia

class Cliente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    barbearia = models.ForeignKey(Barbearia, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
