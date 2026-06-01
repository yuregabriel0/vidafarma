from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout  
from produtos.models import Produto
from estoque.models import Lote, Movimentacao      #o render pega o html e entrega a requisicão // #o redirect manda o usuario para outra página

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
        
def home_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    contexto = {
        "total_produtos": Produto.objects.count(),
        "total_lotes": Lote.objects.count(),
        "estoque_baixo": Produto.objects.filter(qtd_est__lte=10).count(),
        "vencem_30_dias": 0,

        "ultimas_movimentacoes": Movimentacao.objects.select_related(
            "lote",
            "lote__produto",
            "funcionario"
        ).order_by("-data")[:5],
    }

    return render(request, "home.html", contexto)

def produtos_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "produtos.html")

    
def estoque_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "estoque.html")


def controle_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "controle.html")

def movimentacoes_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "movimentacoes.html")    

def logout_view(request):

    logout(request)

    return redirect("login")    