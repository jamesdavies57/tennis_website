from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CompForm

@login_required
def staff_view(request):
    if request.user.account_type != "STAFF":
        return redirect("home")

    return render(request, "staff/staff.html")

@login_required
def comp_results(request):
    if request.user.account_type != "STAFF":
        return redirect("home")
    if request.method == "POST":
        form = CompForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            session = form.cleaned_data["session"]
            bookings = session.bookings.all()
            players = [b.user for b in bookings]
            result.player1 = players[0]
            result.player2 = players[1]
            result.booking = bookings.first()
            result.recorded_by = request.user

            result.save()
            return redirect("comp_results")
    else:
        form = CompForm()

    return render(request, "staff/comp_results.html", {"form": form,})