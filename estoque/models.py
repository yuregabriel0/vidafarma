from django.db import models
from produtos.models import Produto
from usuarios.models import Funcionario

class Lote(models.Model):

    id_lote = models.CharField(
    max_length=20,
    primary_key=True
)

    validade = models.DateField()

    qtd_lote = models.IntegerField()

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Lote {self.id_lote}"

        
class Movimentacao(models.Model):

    id_movimentacao = models.AutoField(
        primary_key=True
    )

    TIPOS = [
    ("entrada", "Entrada"),
    ("saida", "Saída"),]

    tipo = models.CharField(
    max_length=7,
    choices=TIPOS)

    MOTIVOS = [
    ("reposicao", "Reposição"),
    ("venda", "Venda"),
    ("devolucao", "Devolução"),
    ("vencido", "Produto Vencido"),]

    motivo = models.CharField(
    max_length=20,
    choices=MOTIVOS) 

    data = models.DateField()

    quantidade = models.IntegerField()

    lote = models.ForeignKey(
        Lote,
        on_delete=models.CASCADE
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.tipo} - {self.quantidade}"