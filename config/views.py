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

        hoje = date.today()

    vencem_30_dias = Lote.objects.filter(
    validade__gte=hoje,
    validade__lte=hoje + timedelta(days=30)
).count()

    contexto = {
        "total_produtos": Produto.objects.count(),
        "total_lotes": Lote.objects.count(),
        "estoque_baixo": Produto.objects.filter(qtd_est__lte=10).count(),
        "vencem_30_dias": vencem_30_dias,

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
    categoria_filtro = request.GET.get("categoria_filtro")
    status_filtro = request.GET.get("status_filtro")

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

    produtos_lista = Produto.objects.select_related(
        "categoria"
    ).all()

    if pesquisa:

        produtos_lista = produtos_lista.filter(
            nom_produto__icontains=pesquisa
        )

    if categoria_filtro:

        produtos_lista = produtos_lista.filter(
            categoria__id_categoria=categoria_filtro
        )

    if status_filtro == "ativo":

        produtos_lista = produtos_lista.filter(
            qtd_est__gt=0
        )

    elif status_filtro == "inativo":

        produtos_lista = produtos_lista.filter(
            qtd_est=0
        )

    paginator = Paginator(produtos_lista, 10)

    page = request.GET.get("page")

    produtos = paginator.get_page(page)

    categorias = Categoria.objects.all()

    hoje = date.today()

    vencem_30_dias = Lote.objects.filter(
    validade__gte=hoje,
    validade__lte=hoje + timedelta(days=30)
).count()

    contexto = {
        "produtos": produtos,

        "categorias": categorias,

        "vencem_30_dias": vencem_30_dias,

        "total_produtos": Produto.objects.count(),

        "produtos_ativos": Produto.objects.filter(
            qtd_est__gt=0
        ).count(),

        "estoque_baixo": Produto.objects.filter(
            qtd_est__lte=10
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

    pesquisa = request.GET.get("pesquisa")

    categoria_filtro = request.GET.get(
    "categoria_filtro"
)    
    if categoria_filtro:

     lotes = lotes.filter(
        produto__categoria__id_categoria=
        categoria_filtro
    )

    lotes = Lote.objects.select_related(
        "produto",
        "produto__categoria"
    ).all()

    if pesquisa:

     lotes = lotes.filter(

        Q(
            produto__nom_produto__icontains=
            pesquisa
        )

        |

        Q(
            produto__cod_prod__icontains=
            pesquisa
        )

        |

        Q(
            id_lote__icontains=
            pesquisa
        )

    )

    categorias = Categoria.objects.all()

    produtos = Produto.objects.select_related(
        "categoria"
    ).all()

    valor_total = sum(
        produto.preco * produto.qtd_est
        for produto in produtos
    )
    hoje = date.today()

    vencem_30_dias = Lote.objects.filter(
    validade__gte=hoje,
    validade__lte=hoje + timedelta(days=30)
).count()

    valor_total = sum(
    produto.preco * produto.qtd_est
    for produto in produtos
)

    paginator = Paginator(lotes, 5)

    page = request.GET.get("page")

    lotes = paginator.get_page(page)

    contexto = {

        "lotes": lotes,

        "total_produtos": Produto.objects.count(),

        "vencem_30_dias": vencem_30_dias,

        "valor_total": valor_total,

        "estoque_baixo": Produto.objects.filter(
            qtd_est__lte=10
        ).count(),

        "produtos_inativos": Produto.objects.filter(
            qtd_est=0
        ).count(),

        "categorias": categorias,
    }

    return render(
        request,
        "estoque.html",
        contexto
    )


def controle_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    pesquisa = request.GET.get("pesquisa")

    funcionario_filtro = request.GET.get(
        "funcionario_filtro"
    )

    if request.method == "POST":

        produto = Produto.objects.get(
            cod_prod=request.POST.get("produto")
        )

        funcionario = Funcionario.objects.get(
            usuario=request.user
        )

        quantidade = int(
            request.POST.get("qtd_item")
        )

        Lote.objects.create(

            id_lote=request.POST.get("id_lote"),

            validade=request.POST.get(
                "validade"
            ),

            qtd_item=quantidade,

            produto=produto,

            funcionario=funcionario
        )

        produto.qtd_est += quantidade

        produto.save()

        return redirect("controle")

    produtos = Produto.objects.all()

    lotes = Lote.objects.select_related(
        "produto",
        "funcionario"
    ).all()

    if pesquisa:

        lotes = lotes.filter(

            Q(id_lote__icontains=pesquisa)

            |

            Q(
                produto__nom_produto__icontains=pesquisa
            )

        )

    if funcionario_filtro:

        lotes = lotes.filter(
            funcionario__matricula=
            funcionario_filtro
        )

    hoje = date.today()

    lotes_ativos = lotes.count()

    lotes_validos = lotes.filter(
        validade__gte=hoje
    ).count()

    vencem_30_dias = lotes.filter(
        validade__gte=hoje,
        validade__lte=hoje + timedelta(days=30)
    ).count()

    lotes_vencidos = lotes.filter(
        validade__lt=hoje
    ).count()

    paginator = Paginator(lotes, 5)

    page = request.GET.get("page")

    lotes = paginator.get_page(page)

    contexto = {

        "produtos": produtos,

        "lotes": lotes,

        "funcionarios": Funcionario.objects.all(),

        "hoje": hoje,

        "proximos_30_dias":
        hoje + timedelta(days=30),

        "lotes_ativos": lotes_ativos,

        "lotes_validos": lotes_validos,

        "vencem_30_dias": vencem_30_dias,

        "lotes_vencidos": lotes_vencidos,
    }

    return render(
        request,
        "controle.html",
        contexto
    )

def movimentacoes_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "movimentacoes.html")    

def logout_view(request):

    logout(request)

    return redirect("login")    