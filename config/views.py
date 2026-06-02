from django.shortcuts import render, redirect  #o render pega o html e entrega a requisicão // #o redirect manda o usuario para outra página
from django.contrib.auth import authenticate, login, logout  
from produtos.models import Produto
from estoque.models import Lote, Movimentacao
from produtos.models import Produto 
from produtos.models import Produto, Categoria

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

    pesquisa = request.GET.get("pesquisa")

    if request.method == "POST":

        categoria = Categoria.objects.get(
            id_categoria=request.POST.get("categoria")
        )

        Produto.objects.create(
            cod_prod=request.POST.get("cod_prod"),
            nom_produto=request.POST.get("nom_produto"),
            preco=request.POST.get("preco"),
            qtd_est=0,
            categoria=categoria
        )

        return redirect("produtos")

    produtos = Produto.objects.select_related(
        "categoria"
    ).all()

    if pesquisa:

        produtos = produtos.filter(
            nom_produto__icontains=pesquisa
        )

    categorias = Categoria.objects.all()

    contexto = {
        "produtos": produtos,
        "categorias": categorias,

        "total_produtos": Produto.objects.count(),

        "produtos_ativos": Produto.objects.filter(
            qtd_est__gt=0
        ).count(),

        "estoque_baixo": Produto.objects.filter(
            qtd_est__lte=10
        ).count(),

        "produtos_inativos": Produto.objects.filter(
            qtd_est=0
        ).count(),
    }

    return render(
        request,
        "produtos.html",
        contexto
    )

    
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