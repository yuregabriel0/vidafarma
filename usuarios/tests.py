from django.contrib.auth.models import User
from django.test import TestCase

from usuarios.models import Funcionario


class FuncionarioTest(TestCase):

    def test_criar_funcionario(self):

        usuario = User.objects.create_user(username="teste", password="123")

        funcionario = Funcionario.objects.create(
            usuario=usuario,
            matricula="00000001",
            nome="João",
            sobrenome="Silva",
            cargo="Farmacêutico",
        )

        self.assertEqual(funcionario.nome, "João")
