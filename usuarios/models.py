from django.contrib.auth.models import User
from django.db import models


class Funcionario(models.Model):

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    matricula = models.CharField(max_length=8, primary_key=True)

    nome = models.CharField(max_length=20)

    sobrenome = models.CharField(max_length=20)

    cargo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
