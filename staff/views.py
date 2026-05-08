from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CompForm, StaffCreationForm
from bookings.models import Session
from accounts.models import Account, Notification
from .service import generate_court_sessions
from datetime import datetime

@login_required
def staff_view(request):
    user = request.user
    if request.user.account_type != "STAFF":
        return redirect("home")

    return render(request, "staff/staff.html", {"user": user})

@login_required
def comp_results(request):
    #default value for players
    players = None
    #ensure only staff can access page
    if request.user.account_type != "STAFF":
        return redirect("home")
    if request.method == "POST":
        form = CompForm(request.POST)
        session_id = request.POST.get("session")
        #get values from session
        if session_id:
            try:
                session = Session.objects.get(id=session_id)
                bookings = session.bookings.all()
                players = [b.user for b in bookings]
            except Session.DoesNotExist:
                players = None
        if form.is_valid():
            result = form.save(commit=False)
            
            if not players or len(players) != 2:
                return render(request, "staff/comp_results.html", {"form": form,"players": players})

            result.session = session
            result.player1 = players[0]
            result.player2 = players[1]
            result.recorded_by = request.user
            result.save()
            return redirect("comp_results")
    else:
        form = CompForm()

    return render(request, "staff/comp_results.html", {"form": form,"players": players})

@login_required
def user_management(request):
    if request.user.account_type != "STAFF":
        return redirect("home")
    members = (Account.objects.filter(account_type = "MEMBER"))
    return render(request, "staff/user_management.html", {"members": members})

@login_required
def manage_a_user(request, user_id):
    if request.user.account_type != "STAFF":
        return redirect("home")
    
    member = get_object_or_404(Account, id=user_id)
    warnings = (Notification.objects.filter(user=member.id, notif_type = "WARNING"))
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "warn":
            warning_text = request.POST.get("warning_text", "").strip()

            if warning_text:
                Notification.objects.create(user=member,notif_type="WARNING",title="Warning from staff",body=warning_text)
                member.unread_notifs += 1
                member.save()

        elif action == "ban":
            member.is_active = False
            member.membership_status = "CANCELLED"
            member.save()

        return redirect("manage_a_user", user_id=member.id)

    return render(request, "staff/manage_a_user.html", {"member": member, "warnings": warnings})

@login_required
def announcements(request):
    if request.user.account_type != "STAFF":
        return redirect("home")
    
    if request.method == "POST":
        announcement_type = request.POST.get("announcement_type")
        notif_text = request.POST.get("notif_text")
        notif_title = request.POST.get("notif_title")
        if announcement_type == "ALL":
            users = (Account.objects.all())
            notif_type = "ANNOUNCEMENTS"
        elif announcement_type == "PREMIUM":
            users = (Account.objects.filter(membership_type = "PREMIUM"))
            notif_type = "ANNOUNCEMENTS"
        elif announcement_type == "STAFF":
            users = (Account.objects.filter(account_type = "STAFF"))
            notif_type = "STAFF"
        else:
            users = Account.objects.none()
            notif_type = "OTHER"
        for u in users:
            Notification.objects.create(user=u,notif_type=notif_type,title=f"New announcement: {notif_title}",body=notif_text)
            u.unread_notifs += 1
            u.save()
        return redirect("announcements")
    return render(request, "staff/announcements.html")

@login_required
def staff_signup(request):
    if request.user.is_superuser == True:
        if request.method == "POST":
            form = StaffCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("staff")
        else:
            form = StaffCreationForm()
    else:
        return redirect("home")

    return render(request, "staff/staff_signup.html", {"form": form})


@login_required
def staff_management(request):
    if request.user.is_superuser != True:
        return redirect("staff")
    members = (Account.objects.filter(account_type = "STAFF", is_superuser = False))
        
    return render(request, "staff/staff_management.html", {"members": members})

@login_required
def manage_a_staff(request, user_id):
    if request.user.is_superuser != True:
        return redirect("home")
    
    member = get_object_or_404(Account, id=user_id)
    warnings = (Notification.objects.filter(user=member.id, notif_type = "STAFF"))
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "warn":
            warning_text = request.POST.get("warning_text", "").strip()

            if warning_text:
                Notification.objects.create(user=member,notif_type="STAFF",title="Warning from management",body=warning_text)
                member.unread_notifs += 1
                member.save()

        elif action == "ban":
            member.is_active = False
            member.membership_status = "CANCELLED"
            member.save()

        return redirect("manage_a_staff", user_id=member.id)

    return render(request, "staff/manage_a_staff.html", {"member": member, "warnings": warnings})


@login_required
def generate_sessions_view(request):
    if request.user.is_superuser != True:
        return redirect("home")
    if request.method == "POST":
        weeks = int(request.POST.get("weeks", 4))
        start_hour = int(request.POST.get("start_hour", 10))
        end_hour = int(request.POST.get("end_hour", 22))
        start_date_str = request.POST.get("start_date")

        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        else:
            start_date = None

        created = generate_court_sessions(
            weeks=weeks,
            start_hour=start_hour,
            end_hour=end_hour,
            start_date=start_date,
        )
        return redirect("generate_sessions")

    return render(request, "staff/generate_sessions.html")