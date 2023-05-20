from cryptography.fernet import Fernet
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


def encrypt(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode('utf-8'))
    return encrypted_message.decode('utf-8')


def decrypt(message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(message.encode('utf-8'))
    return decrypted_message.decode('utf-8')


def check_key(user1, user2):
    if Friends.objects.get(user=user1, friend=user2).encryption_key == "":
        friends = Friends.objects.get(user=user1, friend=user2)
        friends.encryption_key = Fernet.generate_key()
        friends.encryption_key = friends.encryption_key.decode('utf-8')
        friends.save()
        friends1 = Friends.objects.get(user=user2, friend=user1)
        friends1.encryption_key = friends.encryption_key
        friends1.save()
    return Friends.objects.get(user=user1, friend=user2).encryption_key


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
            print(sender, receiver)
            print(message.sender_name, message.receiver_name)
            sender = User.objects.get(id=sender)
            receiver = User.objects.get(id=receiver)
            key = check_key(sender, receiver).encode('utf-8')
            message.message = decrypt(message.message, key)
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        # breakpoint()
        data = JSONParser().parse(request)

        sender = User.objects.get(username=data["sender_name"])
        receiver = User.objects.get(username=data["receiver_name"])
        key = check_key(sender, receiver).encode('utf-8')
        data["message"] = encrypt(data["message"], key)
        print("DATA: ", data)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
