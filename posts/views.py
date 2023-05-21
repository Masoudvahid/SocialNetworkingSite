from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.http import HttpResponse, JsonResponse, Http404
from .models import Post
from .forms import PostForm
from accounts.models import User

from django.contrib import messages

import json


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_on = timezone.now()
            post.save()
            return redirect('news')
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})


def posts_to_list(posts, user):
    context = []
    for post in posts:
        context.append({
            'id': post.id,
            'author': post.author.username,
            'content': post.content,
            'created_on': post.created_on,
            'likes': post.likes.count(),
            'liked': user in post.likes.all()
        })
    return context


@api_view(['GET'])
def posts_view(request):
    """
    return all the posts
    """
    if not request.user.is_authenticated:
        return redirect("login")
    posts = Post.objects.filter(author=request.user)

    posts = posts_to_list(posts, request.user)

    context = {"posts": posts, 'username': request.user.username}

    return render(request, "posts/profile_posts.html", context)


@api_view(['GET'])
def news(request):
    """
    return all the posts
    """
    if not request.user.is_authenticated:
        return redirect("login")
    posts = Post.objects.all()

    posts = posts_to_list(posts, request.user)
    context = {"posts": posts, 'username': request.user.username}

    return render(request, "posts/news.html", context)


def delete_post(request, id_post):
    """
    Delete post by id, here id is the id of the post in Post table
    """
    print("delete post ", id_post)
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        post = Post.objects.get(pk=id_post)
    except Post.DoesNotExist:
        return Response(data={'error': {'message': 'Post was not found'}}, status=404)

    if post.author != request.user:
        return Response(
            data={'error': {'message': 'You are not allow to delete this post'}}, status=401)

    post.delete()
    return redirect('my_posts')


def like_post(request, id_post):
    """
    Like a post
    """
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        post = Post.objects.get(pk=id_post)
    except Post.DoesNotExist:
        return Response(data={'error': {'message': 'Post was not found'}}, status=404)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('news')


def pop_up(request, id_post):
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        post = Post.objects.get(pk=id_post)
    except Post.DoesNotExist:
        return Response(data={'error': {'message': 'Post was not found'}}, status=404)

    liked_users = [user.username for user in post.likes.all()]
    liked_users = ', '.join(liked_users)

    if liked_users:
        messages.success(request, liked_users)

    return redirect('news')
