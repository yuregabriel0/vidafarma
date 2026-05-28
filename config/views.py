from django.shortcuts import render, redirect        #o render pega o html e entrega a requisicão // #o redirect manda o usuario para outra página

def login_view(request):    #o request é a solicitação do usuário, o que ele quer acessar
    
    erro = ""

    if request.method == "POST":                     #se o método for POST, ou seja, se o usuário enviar um formulário
        matricula = request.POST.get("matricula")    #pega o valor do campo username
        senha = request.POST.get("senha")            #pega o valor do campo password
        
        if matricula == "1" and senha == "1": #se o username for x e a senha for y
            request.session["usuario"] = matricula #cria uma sessão para o usuário, armazenando a matrícula
            return redirect("home") #então redireciona para a página home
        else:
            erro = "Matrícula ou senha incorretos." #se não, mostra uma mensagem de erro    
            
    return render(request, "login.html", {"erro": erro}) #mostra mensagem de erro


def home_view(request):

    if "usuario" not in request.session:
        return redirect("login")
    return render(request, "home.html")



def produtos_view(request):

    if "usuario" not in request.session:
        return redirect("login")

    return render(request, "produtos.html")

    
def estoque_view(request):

    if "usuario" not in request.session:
        return redirect("login")

    return render(request, "estoque.html")


def controle_view(request):
    if "usuario" not in request.session:
        return redirect("login")

    return render(request, "controle.html")

def movimentacoes_view(request):
    if "usuario" not in request.session:
        return redirect("login")

    return render(request, "movimentacoes.html")    