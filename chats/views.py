from django.shortcuts import render, redirect

from .models import Messages
from accounts.models import User, Friends
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chats.serializers import MessageSerializer
from mainpage.views import get_friend_list


def chats(request):
    if request.user.is_authenticated:
        friends_list = get_friend_list(request.user)
        return render(request, "chats/chats_list.html", {"friends": friends_list})
    else:
        return redirect("login")


def chat(request, username):
    friend = User.objects.get(username=username)
    id_user = request.user.id
    curr_user = request.user
    messages = Messages.objects.filter(
        sender_name=id_user, receiver_name=friend.id
    ) | Messages.objects.filter(sender_name=friend.id, receiver_name=id_user)
    context = {"messages": messages, "curr_user": curr_user, "friend": friend}
    if request.method == "GET":
        return render(request, "chats/chats.html", context)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "GET":
        # breakpoint()
        messages = Messages.objects.filter(
            sender_name=sender, receiver_name=receiver, seen=False
        )
        serializer = MessageSerializer(
            messages, many=True, context={"request": request}
        )
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
