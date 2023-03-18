from django.shortcuts import render, redirect
from login.models import User


def search_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    # <input type="text" name="q"/>
    search_query = request.GET.get("q")

    if search_query is not None:
        # Using filter will return multiple rows
        # icontains doesn't care about lower case and upper case
        if len(search_query) > 0:
            search_results = User.objects.filter(username__icontains=search_query)
            accounts = []
            for account in search_results:
                # False for not friends, True for friends
                accounts.append((account, False))
            if len(accounts) == 0:
                error = "Can not find such users"
                context = {"title": "Search", "accounts": accounts, "error": error}
            else:
                context = {"title": "Search", "accounts": accounts}
        else:
            error = "Please pass something to search"
            context = {"title": "Search", "error": error}

    return render(request, "search/search.html", context)
