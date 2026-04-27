from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from accounts.models import Notification

@login_required
def social_home(request):
    post_type = request.GET.get("type")
    if post_type:
        if post_type == "MINE":
            posts = Post.objects.filter(user=request.user).order_by("-upload_time")
        else:
            posts = Post.objects.filter(post_type=post_type).order_by("-upload_time")
    else:
        posts = Post.objects.all().order_by("-upload_time")
    return render(request, "social/social_home.html", {"posts": posts, "current_type": post_type})

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

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        new_comment_body = request.POST.get("body")
        user = request.user
        op = post.user
        
        if new_comment_body:
            #create the comment
            Comment.objects.create(post=post,user=user,body=new_comment_body)

            #prepare and create notification for original poster
            notif_text = f"{user.username} commented on your post '{post.title}': {new_comment_body}"
            Notification.objects.create(user = op, notif_type = "SOCIAL", title = "New comment on your post", body = notif_text)
            op.unread_notifs += 1
            op.save()
            return redirect("view_post", post_id=post_id)
    
    return redirect("view_post", post_id=post_id)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        if request.user.account_type == "STAFF" or post.user == request.user:
                post.delete()
    return redirect("social_home")

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        if request.user.account_type == "STAFF" or comment.user == request.user:
                comment.delete()
    return redirect("view_post", post_id=comment.post.id)