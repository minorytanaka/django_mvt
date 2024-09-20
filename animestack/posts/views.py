from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect

from posts.models import Post
from posts.forms import PostForm


User = get_user_model()


def index(request):
    post_list = (
        Post.objects.select_related("author", "group")
        .defer("group__title", "group__description")
        .order_by("-pub_date")
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    posts = (
        Post.objects.select_related("author", "group")
        .filter(group__slug=slug)
        .annotate(posts_count=Count("group__posts"))
    )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    group_title = posts[0].group.title if posts else None
    group_description = posts[0].group.description if posts else None
    posts_count = posts[0].posts_count if posts else None
    context = {
        "page_obj": page_obj,
        "group_title": group_title,
        "group_description": group_description,
        "posts_count": posts_count,
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    author = User.objects.annotate(posts_count=Count("posts")).get(username=username)
    posts = (
        Post.objects.filter(author=author)
        .select_related("author", "group")
        .order_by("-pub_date")
    )
    posts_list = list(posts)
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"author": author, "page_obj": page_obj}
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = Post.objects.select_related("author", "group").get(pk=post_id)
    context = {"post": post}
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:post_detail", post_id=post.pk)
    form = PostForm()
    context = {"form": form}
    return render(request, "posts/create_post.html", context)


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)

    # Если это POST-запрос, то форма должна обрабатывать данные
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:post_detail", post_id=post_id)
    else:
        # Если это GET-запрос, форма инициализируется данными поста
        form = PostForm(instance=post)

    context = {"form": form, "post": post, "is_edit": True}
    return render(request, "posts/create_post.html", context)
