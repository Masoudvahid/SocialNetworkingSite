from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import User
from django.conf import settings
from .forms import AccountUpdateForm


def profile_view(request, *args, **kwargs):
    context = {}
    username = kwargs.get("username")

    # user is the user we get from the url
    # current_user is the user we get from the request

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("That user doesn't exist.")

    # Fields that are shown in the profile page
    if user:
        context["username"] = user.username
        context["first_name"] = user.first_name
        context["last_name"] = user.last_name
        context["email"] = user.email
        context["phone"] = user.phone
        context["bio"] = user.bio

    # Is this your profile or other profiles?
    is_self = True
    is_friend = True
    current_user = request.user

    if current_user.is_authenticated and current_user != user:
        is_self = False
    elif not current_user.is_authenticated:
        is_self = False

    context["title"] = user
    context["is_self"] = is_self
    context["is_friend"] = is_friend
    context["BASE_URL"] = settings.BASE_URL

    return render(request, "profiles/profile.html", context)


def edit_profile_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")

    username = kwargs.get("username")
    user = User.objects.get(username=username)

    if user.username != request.user.username:
        return HttpResponse("You can not edit someone else profile")

    context = {"title": "Edit profile"}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            form.clean_email()
            return redirect("profile:view", username=user.username)
        else:
            form = AccountUpdateForm(
                request.POST,
                instance=request.user,
                initial={
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "bio": user.bio,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            )
            context["form"] = form
    else:
        form = AccountUpdateForm(
            initial={
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "bio": user.bio,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
    context["form"] = form
    return render(request, "profiles/edit_profile.html", context)
