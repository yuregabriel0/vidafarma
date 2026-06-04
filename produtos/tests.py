from django.test import TestCase
from produtos.models import Categoria, Produto

class ProdutoTest(TestCase):

    def test_criar_produto(self):

        categoria = Categoria.objects.create(
            nome_cat="Genérico"
        )

        produto = Produto.objects.create(

            cod_prod="1234",

            nom_produto="Dipirona",

            preco=10.00,

            qtd_est=100,

            categoria=categoria
        )

        self.assertEqual(
            produto.nom_produto,
            "Dipirona"
        )
