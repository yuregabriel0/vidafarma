from django.shortcuts import render, redirect  #o render pega o html e entrega a requisicão // #o redirect manda o usuario para outra página
from django.contrib.auth import authenticate, login, logout  
from produtos.models import Produto
from estoque.models import Lote, Movimentacao
from produtos.models import Produto 
from produtos.models import Produto, Categoria
from usuarios.models import Funcionario
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.db.models import Q
from django.contrib import messages

def login_view(request):

    erro = ""

    if request.method == "POST":

        matricula = request.POST.get("matricula")
        senha = request.POST.get("senha")

        user = authenticate(
            request,
            username=matricula,
            password=senha
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            erro = "Matrícula ou senha incorretos."

    return render(request, "login.html", {"erro": erro})


def logout_view(request):

    logout(request)

    return redirect("login") 