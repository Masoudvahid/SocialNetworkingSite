from django.shortcuts import render, redirect


def home_view(request):
    if request.user.is_authenticated:
        name = request.user.first_name + " " + request.user.last_name
        return render(request, "home.html", {"name": name})
    else:
        return redirect("login")
