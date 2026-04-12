from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Notification

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})

@login_required
def account(request):
    return render(request, "accounts/account.html")

@login_required
def notifications(request):
    curr_user=request.user
    notifs = Notification.objects.filter(user=curr_user).order_by("-time")
    return render(request, "accounts/notifications.html", {"notifications": notifs})