from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.db import models

from .models import Session
from .facade import create_booking

@login_required
def session_list(request):
    sessions = (
        Session.objects.annotate(num_bookings=Count("bookings")).filter(num_bookings__lt=models.F("max_players")).order_by("start_time"))

    return render(request, "bookings/session_list.html", {"sessions": sessions})

@login_required
def book_session_page(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    if request.method == "POST":
        try:
            create_booking(user=request.user, session=session)
            messages.success(request, "Booking successful!")
            return redirect("session_list")
        except Exception as e:
            messages.error(request, str(e))

    return render(request, "bookings/book_session.html", {"session": session})