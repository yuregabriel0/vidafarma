from django.db import models

class Funcionario(models.Model):

    matricula = models.CharField(
    max_length=8,
    primary_key=True
)

    nome = models.CharField(
        max_length=20
    )

    sobrenome = models.CharField(
        max_length=20
    )

    cargo = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.nome