from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import User
from django.conf import settings
from .forms import AccountUpdateForm
from accounts.models import Friends
from chats.views import get_friends_list


def check_friendship(user_1, user_2):
    if Friends.objects.filter(user=user_1, friend=user_2).exists():
        return not Friends.objects.get(user=user_1, friend=user_2).is_request
    elif Friends.objects.filter(user=user_2, friend=user_1).exists():
        return not Friends.objects.get(user=user_2, friend=user_1).is_request
    return False


def profile_view(request, *args, **kwargs):
    context = {}
    username = kwargs.get("username")

    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("That user doesn't exist.")

    if user_profile:
        context["username"] = user_profile.username
        context["first_name"] = user_profile.first_name
        context["last_name"] = user_profile.last_name
        context["email"] = user_profile.email
        context["phone"] = user_profile.phone
        context["bio"] = user_profile.bio

    is_self = True
    current_user = request.user
    is_logged_in = current_user.is_authenticated

    if not is_logged_in:
        is_self = False
    elif current_user.username != username:
        is_self = False

    is_friend = check_friendship(current_user, user_profile)

    # For status requested 0 = not requested, 1 = requested by me, 2 = requested by other
    context["status_request"] = 0
    if Friends.objects.filter(user=current_user, friend=user_profile).exists():
        context["status_request"] = 1 if Friends.objects.get(user=current_user, friend=user_profile).is_request else 0
    elif Friends.objects.filter(user=user_profile, friend=current_user).exists():
        context["status_request"] = 2 if Friends.objects.get(user=user_profile, friend=current_user).is_request else 0
    context["title"] = user_profile
    context["is_self"] = is_self
    context["is_logged_in"] = is_logged_in
    context["is_friend"] = is_friend
    context["BASE_URL"] = settings.BASE_URL

    return render(request, "profiles/profile.html", context)


def add_friend(request, username):
    if not request.user.is_authenticated:
        return redirect("login")

    friend = User.objects.get(username=username)
    user = User.objects.get(username=request.user.username)

    # If the friend has sent a friend request
    if Friends.objects.filter(user=friend, friend=user).exists():
        friendship = Friends.objects.get(user=friend, friend=user)
        friendship.is_request = False
        friendship.save()
        friendship = Friends(user=user, friend=friend)
        friendship.is_request = False
        friendship.save()
        print("Friend added")

    # No relationship exists
    if not Friends.objects.filter(user=user, friend=friend).exists():
        friendship = Friends(user=user, friend=friend, is_request=True)
        friendship.save()
        print("Request sent")
    else:
        print("Friend already exists")

    return redirect("profile:view", username=friend.username)


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
