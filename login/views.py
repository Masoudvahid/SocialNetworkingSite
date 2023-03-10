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


def register_view(request):
    form = RegisterForm(request.POST or None)
    context = {"title": "Register!", "form": form}

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        if form.is_valid():
            form.save()
            # Add a success message in the future if possible
            return redirect("login")
        else:
            # I want to change this
            # each error comes as a list of one string, and i extract the string using [0]
            # It could be done better
            context["errors"] = [error[0] for error in form.errors.values()]
    return render(request, "login/register.html", context=context)


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy("login"))
