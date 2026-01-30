from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Session, Booking
from accounts.models import Account

#facade to help to create bookings
def create_booking(*, user: Account, session: Session) -> Booking:

    if session.bookings.count() >= session.max_players:
        raise ValidationError("This session is full.")

    if Booking.objects.filter(user=user, session=session).exists():
        raise ValidationError("You are already booked into this session.")

    #competitive rules
    if session.session_type == "COMPETITIVE":
        if user.membership_type != "PREMIUM":
            raise ValidationError("Only premium members can join competitive sessions.")

        if user.membership_status != "ACTIVE":
            raise ValidationError("Your membership is not active.")

        if user.competitive_rank is None:
            raise ValidationError("You do not have a competitive rank.")

    with transaction.atomic():
        booking = Booking.objects.create(
            user=user,
            session=session
        )

    return booking
