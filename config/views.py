from django.shortcuts import render #o render pega o html e entrega a requisicão 

def login_view(request): #o request é a solicitação do usuário, o que ele quer acessar
    return render(request, "login.html")


def home_view(request):
    return render(request, "home.html")



def produtos_view(request):
    return render(request, "produtos.html")

    
def estoque_view(request):
    return render(request, "estoque.html")


def controle_view(request):
    return render(request, "controle.html")