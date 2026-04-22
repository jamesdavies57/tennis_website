from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import Notification
from bookings.models import Comp_results
from django.db.models import Q

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
    #reset unread notifs
    curr_user.unread_notifs = 0
    curr_user.save()
    return render(request, "accounts/notifications.html", {"notifications": notifs})

@login_required
def my_details(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("details")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "accounts/details.html", {"form": form,"user": request.user,})

@login_required
def match_history(request):
    if request.user.membership_type != "PREMIUM":
        return redirect("home")
    curr_user=request.user
    #query to get all matches of current user with no duplciates
    matches = Comp_results.objects.filter(Q(player1=curr_user) | Q(player2=curr_user)).order_by("-time")
    return render(request, "accounts/matches.html", {"matches": matches})