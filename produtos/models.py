from django.db import models


class Categoria(models.Model):

    id_categoria = models.AutoField(primary_key=True)

    nome_cat = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_cat


class Produto(models.Model):

    cod_prod = models.CharField(max_length=6, primary_key=True)

    nom_produto = models.CharField(max_length=50)

    preco = models.DecimalField(max_digits=10, decimal_places=2)

    qtd_est = models.IntegerField()

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_produto
