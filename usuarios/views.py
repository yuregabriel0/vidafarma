from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def login_view(request):

    erro = ""

    if request.method == "POST":

        matricula = request.POST.get("matricula")
        senha = request.POST.get("senha")

        user = authenticate(request, username=matricula, password=senha)

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            erro = "Matrícula ou senha incorretos."

    return render(request, "login.html", {"erro": erro})


def logout_view(request):

    logout(request)

    return redirect("login")
