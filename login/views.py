from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

##############################################
# CHANGE VIEWS TO CLASS-BASED VIEWS!!!       #
##############################################


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "login/login.html",
                {"error": "Username or password is incorrect"},
            )
    return render(request, "login/login.html", {"title": "Login!"})


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy("login"))
