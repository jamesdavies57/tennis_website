from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def staff_view(request):

    if request.user.account_type != "STAFF":
        return redirect("home")

    return render(request, "staff/staff.html")