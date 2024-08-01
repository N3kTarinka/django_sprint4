from blog.forms import CommentForm, PostForm, ProfileUpdateForm
from blog.models import Category, Comment, Post
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .constants import REPRESENTATION_LENGTH
from .utils import get_published_posts

User = get_user_model()


def index(request):
    page_obj = get_published_posts()
    paginator = Paginator(page_obj, REPRESENTATION_LENGTH)
    page_number = request.GET.get('page')
    context = {'page_obj': paginator.get_page(page_number)}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        post = get_object_or_404(
            Post,
            pk=post_id,
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    comments = Comment.objects.filter(post_id=post_id).order_by('created_at')
    context = {
        'post': post,
        'comments': comments,
        'form': CommentForm()
    }
    return render(request, 'blog/detail.html', context)


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_user_profile = request.user == profile_user

    if is_user_profile:
        page_obj = Post.objects.filter(author=request.user).annotate(
            comment_count=Count('comments')).order_by('-pub_date')
    else:
        page_obj = get_published_posts().filter(author=profile_user)

    paginator = Paginator(page_obj, REPRESENTATION_LENGTH)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/profile.html', {'profile': profile_user,
                                                 'page_obj': page_obj})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    page_obj = get_published_posts().filter(category__slug=category_slug)

    paginator = Paginator(page_obj, REPRESENTATION_LENGTH)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/category.html', {'page_obj': page_obj,
                                                  'category': category})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user)

    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/create.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user)

    return render(request, 'blog/create.html', {'post': post})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {'form': form})


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    form = CommentForm(request.POST or None, instance=comment)

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {'form': form,
                                                 'comment': comment})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html',
                  {'comment': comment})


@login_required
def edit_profile(request):
    profile_user = get_object_or_404(User, username=request.user)
    form = ProfileUpdateForm(request.POST or None, instance=profile_user)

    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=profile_user.username)

    return render(request, 'blog/user.html', {'form': form})
