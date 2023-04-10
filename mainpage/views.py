from django.shortcuts import render, redirect
from accounts.models import Friends
from django.views.decorators.clickjacking import xframe_options_exempt


def home_view(request):
    if request.user.is_authenticated:
        name = request.user.first_name + " " + request.user.last_name
        return render(request, "mainpage/home.html", {"name": name})
    else:
        return redirect("login")


def get_friend_list(user):
    friends = [friend.friend for friend in Friends.objects.filter(user=user,
                                                                  is_request=False)]
    return friends


@xframe_options_exempt
def friends_bar(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    friends = get_friend_list(user)
    context = {"friends": friends}
    return render(request, "friends_list.html", context)


def view_friends(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    friends = get_friend_list(user)
    context = {"friends": friends}
    return render(request, "friends.html", context)


def get_friends_request(user):
    friends = [friend.user for friend in Friends.objects.filter(friend=user, is_request=True)]
    return friends


def view_friend_requests(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    requests = get_friends_request(user)
    context = {"requests": requests}
    return render(request, "friend_requests.html", context)
