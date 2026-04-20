from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CompForm
from bookings.models import Session

@login_required
def staff_view(request):
    if request.user.account_type != "STAFF":
        return redirect("home")

    return render(request, "staff/staff.html")

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
            result.booking = bookings.first()
            result.recorded_by = request.user
            result.save()
            return redirect("comp_results")
    else:
        form = CompForm()

    return render(request, "staff/comp_results.html", {"form": form,"players": players})