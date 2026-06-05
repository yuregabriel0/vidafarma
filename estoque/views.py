from datetime import date, timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from estoque.models import Lote, Movimentacao
from produtos.models import Categoria, Produto
from usuarios.models import Funcionario


def home_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    hoje = date.today()

    vencem_30_dias = Lote.objects.filter(
        validade__gte=hoje, validade__lte=hoje + timedelta(days=30)
    ).count()

    contexto = {
        "total_produtos": Produto.objects.count(),
        "total_lotes": Lote.objects.count(),
        "estoque_baixo": Produto.objects.filter(qtd_est__lte=10).count(),
        "vencem_30_dias": vencem_30_dias,
        "ultimas_movimentacoes": Movimentacao.objects.select_related(
            "lote", "lote__produto", "funcionario"
        ).order_by("-data")[:5],
    }

    return render(request, "home.html", contexto)


def estoque_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    pesquisa = request.GET.get("pesquisa")

    categoria_filtro = request.GET.get("categoria_filtro")

    produtos = Produto.objects.select_related("categoria").all()

    if pesquisa:

        produtos = produtos.filter(
            Q(nom_produto__icontains=pesquisa)
            | Q(cod_prod__icontains=pesquisa)
            | Q(lote__id_lote__icontains=pesquisa)
        ).distinct()

    if categoria_filtro:

        produtos = produtos.filter(categoria__id_categoria=categoria_filtro)

    valor_total = sum(produto.preco * produto.qtd_est for produto in produtos)

    vencem_30_dias = Lote.objects.filter(
        validade__gte=date.today(), validade__lte=date.today() + timedelta(days=30)
    ).count()

    paginator = Paginator(produtos, 5)

    page = request.GET.get("page")

    produtos = paginator.get_page(page)

    contexto = {
        "produtos": produtos,
        "categorias": Categoria.objects.all(),
        "total_produtos": Produto.objects.count(),
        "valor_total": valor_total,
        "estoque_baixo": Produto.objects.filter(qtd_est__lte=10).count(),
        "vencem_30_dias": vencem_30_dias,
    }

    return render(request, "estoque.html", contexto)


def controle_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    pesquisa = request.GET.get("pesquisa")

    funcionario_filtro = request.GET.get("funcionario_filtro")

    if request.method == "POST":

        produto = Produto.objects.get(cod_prod=request.POST.get("produto"))

        funcionario = Funcionario.objects.get(usuario=request.user)

        quantidade = int(request.POST.get("qtd_item"))

        lote = Lote.objects.create(
            id_lote=request.POST.get("id_lote"),
            validade=request.POST.get("validade"),
            qtd_item=quantidade,
            produto=produto,
            funcionario=funcionario,
        )

        produto.qtd_est += quantidade

        produto.save()

        Movimentacao.objects.create(
            tipo="entrada",
            motivo="reposicao",
            data=date.today(),
            quantidade=quantidade,
            lote=lote,
            funcionario=funcionario,
        )

        return redirect("controle")

    produtos = Produto.objects.all()

    lotes = Lote.objects.select_related("produto", "funcionario").all()

    if pesquisa:

        lotes = lotes.filter(
            Q(id_lote__icontains=pesquisa) | Q(produto__nom_produto__icontains=pesquisa)
        )

    if funcionario_filtro:

        lotes = lotes.filter(funcionario__matricula=funcionario_filtro)

    hoje = date.today()

    lotes_ativos = lotes.count()

    lotes_validos = lotes.filter(validade__gte=hoje).count()

    vencem_30_dias = lotes.filter(
        validade__gte=hoje, validade__lte=hoje + timedelta(days=30)
    ).count()

    lotes_vencidos = lotes.filter(validade__lt=hoje).count()

    paginator = Paginator(lotes, 5)

    page = request.GET.get("page")

    lotes = paginator.get_page(page)

    contexto = {
        "produtos": produtos,
        "lotes": lotes,
        "funcionarios": Funcionario.objects.all(),
        "hoje": hoje,
        "proximos_30_dias": hoje + timedelta(days=30),
        "lotes_ativos": lotes_ativos,
        "lotes_validos": lotes_validos,
        "vencem_30_dias": vencem_30_dias,
        "lotes_vencidos": lotes_vencidos,
    }

    return render(request, "controle.html", contexto)


def movimentacoes_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    pesquisa = request.GET.get("pesquisa")

    funcionario_filtro = request.GET.get("funcionario_filtro")

    tipo_filtro = request.GET.get("tipo")

    if request.method == "POST":

        lote = Lote.objects.get(id_lote=request.POST.get("lote"))

        funcionario = Funcionario.objects.get(usuario=request.user)

        quantidade = int(request.POST.get("quantidade"))

        produto = lote.produto

        if quantidade > lote.qtd_item:

            messages.error(request, "Quantidade maior que o estoque disponível.")

            return redirect("movimentacoes")

        lote.qtd_item -= quantidade

        produto.qtd_est -= quantidade

        Movimentacao.objects.create(
            tipo="saida",
            motivo=request.POST.get("motivo"),
            data=date.today(),
            quantidade=quantidade,
            lote=lote,
            funcionario=funcionario,
        )

        lote.save()

        produto.save()

        return redirect("movimentacoes")

    movimentacoes = Movimentacao.objects.select_related(
        "lote", "lote__produto", "funcionario"
    ).order_by("-data", "-id_movimentacao")

    if pesquisa:

        movimentacoes = movimentacoes.filter(
            Q(lote__produto__nom_produto__icontains=pesquisa)
            | Q(lote__id_lote__icontains=pesquisa)
            | Q(motivo__icontains=pesquisa)
            | Q(data__icontains=pesquisa)
        )

    if funcionario_filtro:

        movimentacoes = movimentacoes.filter(funcionario__matricula=funcionario_filtro)

    if tipo_filtro == "entrada":

        movimentacoes = movimentacoes.filter(tipo="entrada")

    elif tipo_filtro == "saida":

        movimentacoes = movimentacoes.filter(tipo="saida")

    valor_movimentado = sum(
        mov.lote.produto.preco * mov.quantidade for mov in movimentacoes
    )

    contexto = {
        "movimentacoes": movimentacoes,
        "lotes": Lote.objects.select_related("produto").all(),
        "funcionarios": Funcionario.objects.all(),
        "total_entradas": Movimentacao.objects.filter(tipo="entrada").count(),
        "total_saidas": Movimentacao.objects.filter(tipo="saida").count(),
        "total_movimentacoes": Movimentacao.objects.count(),
        "valor_movimentado": valor_movimentado,
    }

    return render(request, "movimentacoes.html", contexto)
