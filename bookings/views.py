from datetime import datetime, time
from django.utils import timezone
from django.db.models import Count, F, Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Session
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Booking
from .facade import cancel_booking, create_booking

#variable for rank difference
RANK_DIFFERENCE = 100

#booking home page
@login_required
def bookings_home(request):
    user = request.user
    is_premium = getattr(user, "membership_type", None) == "PREMIUM"

    return render(request, "bookings/bookings_home.html", {
        "is_premium": is_premium,
    })


#split date input
def _day_bounds(date_str):
    #requires YYYY-MM-DD
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    start = timezone.make_aware(datetime.combine(date, time.min))
    end = timezone.make_aware(datetime.combine(date, time.max))

    return start, end, date


@login_required
def casual_sessions(request):
    date_str = request.GET.get("date")
    #default to today if error
    if not date_str:
        date_str = timezone.localdate().isoformat()

    start, end, _ = _day_bounds(date_str)
    #get available casual sessions by filtering out cancelled and full sessions 
    get_sessions = (Session.objects.filter(court__court_type="CASUAL", is_cancelled=False, start_time__range=(start, end))
                    .annotate(active_bookings=Count("bookings", filter=Q(bookings__cancelled_at__isnull=True)))
                    .filter(active_bookings__lt=F("court__max_players"))
                    .order_by("start_time"))

    return render(request, "bookings/session_list.html", {"sessions": get_sessions,"session_type": "CASUAL","date": date_str,})

@login_required
def competitive_sessions(request):
    date_str = request.GET.get("date")
    if not date_str:
        #default to today
        date_str = timezone.localdate().isoformat()

    start, end, _ = _day_bounds(date_str)
    #filter for not cancelled, not full comp sessions
    get_sessions = (
        Session.objects.filter(court__court_type="COMPETITIVE", is_cancelled=False, start_time__range=(start, end))
        .annotate(active_bookings=Count("bookings", filter=Q(bookings__cancelled_at__isnull=True)))
        .filter(active_bookings__lt=F("court__max_players"))
        .order_by("start_time").distinct()
    )
    #dont display sessions that have too great a rank difference
    if getattr(request.user, "competitive_rank", None) is not None:
        get_sessions = (get_sessions
                        .exclude(bookings__cancelled_at__isnull=True,bookings__user__competitive_rank__lt=request.user.competitive_rank - RANK_DIFFERENCE,)
                        .exclude(bookings__cancelled_at__isnull=True,bookings__user__competitive_rank__gt=request.user.competitive_rank + RANK_DIFFERENCE,)
                        )
    else:
        #if user has no rank, dont show competitive sessions
        get_sessions = get_sessions.none()

    return render(request, "bookings/session_list.html", {"sessions": get_sessions,"session_type": "COMPETITIVE", "date": date_str,})


@login_required
def my_bookings(request):
    #get all upcoming bookings for a user
    now = timezone.now()
    bookings = (
        Booking.objects
        .filter(user=request.user, cancelled_at__isnull=True, session__start_time__gte=now)
        .select_related("session", "session__court")
        .order_by("session__start_time")
    )
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})

@login_required
@require_POST
def cancel_my_booking(request, booking_id):
    #try to find a booking by its ID, if an error is found, call a 404 page
    booking = get_object_or_404(Booking, id=booking_id)
    try:
        cancel_booking(user=request.user, booking=booking)
        messages.success(request, "Booking cancelled.")
    except Exception as e:
        messages.error(request, str(e))
    return redirect("my_bookings")

@login_required
def book_session_page(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    print("book_session_page method =", request.method)

    if request.method == "POST":
        try:
            create_booking(user=request.user, session=session)
            messages.success(request, "Booking successful!")
        except Exception as e:
            messages.error(request, str(e))

        if session.session_type == "CASUAL":
            return redirect("casual_sessions")
        return redirect("competitive_sessions")

    return render(request, "bookings/book_session.html", {"session": session})
