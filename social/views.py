from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment


@login_required
def social_home(request):
    posts = Post.objects.all().order_by("-upload_time")
    return render(request, "social/social_home.html", {"posts": posts})

@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by("upload_time")

    return render(request, "social/view_post.html", {"post": post,"comments": comments,})

@login_required
def create_post(request):
    if request.method == "POST":
        new_post_title = request.POST.get("title")
        new_post_body = request.POST.get("body")
        new_post_type = request.POST.get("post_type", "OTHER")

        if new_post_title and new_post_body and new_post_type:
            Post.objects.create(user=request.user,title=new_post_title,body=new_post_body, post_type=new_post_type)
            return redirect("social_home")
    
    return render(request, "social/create_post.html")
