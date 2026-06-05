from datetime import date, timedelta

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from estoque.models import Lote
from produtos.models import Categoria, Produto


def produtos_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    pesquisa = request.GET.get("pesquisa")
    categoria_filtro = request.GET.get("categoria_filtro")
    status_filtro = request.GET.get("status_filtro")

    if request.method == "POST":

        categoria = Categoria.objects.get(id_categoria=request.POST.get("categoria"))

        Produto.objects.create(
            cod_prod=request.POST.get("cod_prod"),
            nom_produto=request.POST.get("nom_produto"),
            preco=request.POST.get("preco"),
            qtd_est=0,
            categoria=categoria,
        )

        return redirect("produtos")

    produtos_lista = Produto.objects.select_related("categoria").all()

    if pesquisa:

        produtos_lista = produtos_lista.filter(nom_produto__icontains=pesquisa)

    if categoria_filtro:

        produtos_lista = produtos_lista.filter(categoria__id_categoria=categoria_filtro)

    if status_filtro == "ativo":

        produtos_lista = produtos_lista.filter(qtd_est__gt=0)

    elif status_filtro == "inativo":

        produtos_lista = produtos_lista.filter(qtd_est=0)

    paginator = Paginator(produtos_lista, 10)

    page = request.GET.get("page")

    produtos = paginator.get_page(page)

    categorias = Categoria.objects.all()

    hoje = date.today()

    vencem_30_dias = Lote.objects.filter(
        validade__gte=hoje, validade__lte=hoje + timedelta(days=30)
    ).count()

    contexto = {
        "produtos": produtos,
        "categorias": categorias,
        "vencem_30_dias": vencem_30_dias,
        "total_produtos": Produto.objects.count(),
        "produtos_ativos": Produto.objects.filter(qtd_est__gt=0).count(),
        "estoque_baixo": Produto.objects.filter(qtd_est__lte=10).count(),
    }

    return render(request, "produtos.html", contexto)
