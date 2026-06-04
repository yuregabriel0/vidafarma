from django.test import TestCase
from datetime import date
from produtos.models import Categoria, Produto
from usuarios.models import Funcionario
from estoque.models import Lote, Movimentacao
from django.contrib.auth.models import User


class EstoqueTest(TestCase):

    def test_criar_lote(self):

        usuario = User.objects.create_user(
            username="drogaria",
            password="uninassau123"
        )

        funcionario = Funcionario.objects.create(

            usuario=usuario,

            matricula="03265987",

            nome="João",

            sobrenome="Silva",

            cargo="Farmacêutico"
        )

        categoria = Categoria.objects.create(
            nome_cat="Genérico"
        )

        produto = Produto.objects.create(

            cod_prod="4897",

            nom_produto="Dipirona",

            preco=10.00,

            qtd_est=100,

            categoria=categoria
        )

        lote = Lote.objects.create(

            id_lote="L001",

            validade=date(2028, 1, 1),

            qtd_item=50,

            produto=produto,

            funcionario=funcionario
        )

        self.assertEqual(
            lote.qtd_item,
            50
        )
