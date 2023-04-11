from django.shortcuts import render
from django.shortcuts import render, redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.http import HttpResponse, JsonResponse, Http404
from .models import Post
from accounts.models import User
from .serializers import PostSerializer


@api_view(['GET'])
def posts_view(request):
    """
    return all the posts
    """
    if not request.user.is_authenticated:
        return redirect("login")
    posts = Post.objects.filter(author=request.user.username)
    serializer = PostSerializer(posts, many=True)

    data_list = serializer.data

    context = {"posts": data_list}

    return render(request, "posts/profile_posts.html", context)


@api_view(['GET'])
def news(request):
    """
    return all the posts
    """
    if not request.user.is_authenticated:
        return redirect("login")
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)

    data_list = serializer.data

    context = {"posts": data_list}

    return render(request, "posts/news.html", context)


@api_view(['POST'])
def create_post(request):
    """
    Create post
    """
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'POST':
        data = {
            'content': request.data['content'],
            'author': request.user.username,
        }

        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(data={'error': {'message': 'unable to process request'}},
                                status=400)


@api_view(['DELETE'])
def delete_post(request, id):
    """
    Delete post by id, here id is the id of the post in Post table
    """
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        post = Post.objects.get(pk=id)
        if post.author != request.user:
            return JsonResponse(data={'error': {'message': 'You are not allow to delete this post'}}, status=401)
        post.delete()
        return JsonResponse(data={'messages': 'Post was deleted'}, status=200)

    # Can not find this post
    except Post.DoesNotExist:
        return Response(data={'error': {'message': 'Post was not found'}}, status=404)
    # Other errors
    except:
        return Response(data={'error': {'message': 'Something went wrong'}}, status=500)


@api_view(['GET'])
def post_detail(request, id):
    """
        Get the detail of each post by id
    """
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return Response(data={'error': {'message': 'Post was not found'}}, status=404)

    serializer = PostSerializer(post)
    return JsonResponse(serializer.data, status=200, safe=False)


@api_view(['PUT'])
def edit_post(request):
    """
        Edit a post
    """
    if not request.user.is_authenticated:
        return redirect("login")

    # Check the correctness of the request
    try:
        data = {
            'content': request.data['content'],
            'id': request.data['id'],
            'author': request.user.username,
        }
    except:
        return JsonResponse(data={'message': 'Your request is not correct'}, status=400)

    try:
        post = Post.objects.get(pk=data['id'])
        serializer = PostSerializer(post, data=data)

    except Post.DoesNotExist:
        return Response(data={'message': 'Post was not found'}, status=404)

    if post.author != request.user:
        return Response(
            data={'message': 'You are not allow to edit this post'}, status=401)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        return Response(
            data={'message': 'Something went wrong'}, status=400)
