from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
import json

from .forms import RegisterForm, LoginForm


def check_login(request):
    if request.user.is_authenticated:
        return redirect("news")
    else:
        return redirect("login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("news")

    if request.method == "POST":
        if request.accepts("application/json"):
            form = LoginForm(json.loads(request.body) or None)
            context = {"title": "Login!", "form": form}
            if form.is_valid():
                # Could this be done better?
                # Maybe with UserCacheMixin?

                username = json.loads(request.body)['username']
                password = json.loads(request.body)['password']
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return JsonResponse(
                        {"ok": True, "empty_fields": False, "message": "Logged in successfully"})
                else:
                    context["errors"] = [error[0] for error in form.errors.values()]
                    return JsonResponse(
                        {"ok": False, "empty_fields": True, "message": "Invalid username or password"})
            else:
                context["errors"] = [error[0] for error in form.errors.values()]
                return JsonResponse(
                    {"ok": False, "empty_fields": True, "message": "Please enter username and password"})

    return render(request, "login/login.html")


def register_view(request):
    form = RegisterForm(request.POST or None)
    context = {"title": "Register!", "form": form}

    if request.user.is_authenticated:
        return redirect("news")

    if request.method == "POST":
        if request.accepts("application/json"):
            form = RegisterForm(json.loads(request.body) or None)
            context = {"title": "Login!", "form": form}
            if form.is_valid():
                username = json.loads(request.body)['username']
                name = json.loads(request.body)['first_name']
                lastname = json.loads(request.body)['last_name']
                phone = json.loads(request.body)['phone']
                password = json.loads(request.body)['password1']
                password_confirm = json.loads(request.body)['password2']
                email = json.loads(request.body)['email']
                form.save()
                return JsonResponse({"ok": True, "empty_fields": False, "message": "User created successfully"})
            else:
                context["errors"] = [error[0] + '\n' for error in form.errors.values() if
                                     error[0] != 'This field is required.']
                return JsonResponse({"ok": False, "form_error": True, "error": context["errors"]})
    return render(request, "login/register.html")


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy("login"))
