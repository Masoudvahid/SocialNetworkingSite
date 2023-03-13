from django.shortcuts import render, redirect
from .models import Friends, Messages
from login.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chats.serializers import MessageSerializer


def get_friends_list(username):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """
    try:
        user = User.objects.get(username=username)
        friends = Friends.objects.filter(user=user)
        friends_list = []
        for friend in friends:
            friends_list.append(User.objects.get(username=friend.friend.username))
        return friends_list
    except:
        return []


def search(request):
    """
    Search users page
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect("login")
    users = list(User.objects.all())
    for user in users:
        if user.username == request.user.username:
            users.remove(user)
            break

    if request.method == "POST":
        print("SEARCHING!!")
        query = request.POST.get("search")
        user_ls = []
        for user in users:
            if query in user.first_name or query in user.username:
                user_ls.append(user)
        return render(request, "chats/search.html", {'users': user_ls, })

    try:
        users = users[:10]
    except:
        users = users[:]
    friends = get_friends_list(request.user.username)
    not_friends = [element for element in users if element not in friends]
    return render(request, "chats/search.html", {'users': not_friends, 'friends': friends})


def add_friend(request, username):
    """
    Add a user to the friend's list
    :param request:
    :param username:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect("login")

    friend = User.objects.get(username=username)
    user = User.objects.get(username=request.user.username)

    if not Friends.objects.filter(user=user, friend=friend).exists():
        a = Friends(user=user, friend=friend)
        a.save()
        print("Friend added")
    else:
        print("Friend already exists")
    return redirect("/chats/search/")


def chats(request):
    if request.user.is_authenticated:
        friends_list = get_friends_list(username=request.user.username)
        return render(request, "chats/Base.html", {'friends': friends_list})
    else:
        return redirect("login")


def chat(request, username):
    """
    Get the chats between two users.
    :param request:
    :param username:
    :return:
    """
    # breakpoint()

    friend = User.objects.get(username=username)
    id = request.user.id
    curr_user = User.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(
        sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = get_friends_list(request.user.username)
        return render(request, "chats/messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend})


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'GET':
        # breakpoint()
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        # breakpoint()
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
