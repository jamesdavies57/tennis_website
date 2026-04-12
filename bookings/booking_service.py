from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .models import Booking
#extra logic to help to create bookings

#can be tweaked later
RANK_DIFFERENCE = 100

#get all bookings that arent cancelled
def _active_bookings(session):
    return session.bookings.filter(cancelled_at__isnull=True).select_related("user")

def create_booking(*, user, session):
    #validate sessions not been cancelled
    if session.is_cancelled:
        raise ValidationError("This session has been cancelled.")

    #check capacity
    active = _active_bookings(session)
    if active.count() >= session.max_players:
        raise ValidationError("This session is full.")

    #prevent duplicate bookings
    if Booking.objects.filter(user=user, session=session, cancelled_at__isnull=True).exists():
        raise ValidationError("You are already booked into this session.")

    #competitive rules
    if session.session_type == "COMPETITIVE":
        if user.membership_status != "ACTIVE":
            raise ValidationError("Your membership is not active.")
        if user.competitive_rank is None:
            raise ValidationError("You do not have a competitive rank.")

        #player ranks must be within difference
        for booking in active:
            other = booking.user
            if other.competitive_rank is not None:
                if abs(user.competitive_rank - other.competitive_rank) > RANK_DIFFERENCE:
                    raise ValidationError("Your rank is too far from the existing players in this session.")

    #create the booking
    with transaction.atomic():
        booking = Booking.objects.create(user=user, session=session)

    return booking

def cancel_booking(*, user, booking):
    #only staff and the user that created the booking can cancel
    if booking.user_id != user.id and not user.is_staff:
        raise ValidationError("You cannot cancel this booking.")
    if booking.cancelled_at is not None:
        raise ValidationError("Booking is already cancelled.")
    booking.cancelled_at = timezone.now()
    booking.save(update_fields=["cancelled_at"])
    return booking
