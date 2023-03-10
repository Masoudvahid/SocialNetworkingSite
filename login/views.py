from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

from .forms import RegisterForm

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


##############################################
# Too insecure register, make it better yet  #
##############################################


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            print("CHECK THIS\n", form)
            return render(
                request,
                "login/register.html",
                {"error": "Something went wrong"},
            )
    return render(request, "login/register.html", {"form": form, "title": "Register!"})


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy("login"))
