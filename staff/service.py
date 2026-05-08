from datetime import datetime, time, timedelta
from django.utils import timezone
from django.db import transaction

from bookings.models import Court, Session


@transaction.atomic
def generate_court_sessions(weeks=4, start_hour=10, end_hour=22, start_date=None):
    if start_date is None:
        start_date = timezone.localtime().date()

    end_date = start_date + timedelta(weeks=weeks)
    courts = Court.objects.filter(is_active=True)
    created = 0
    day = start_date

    while day < end_date:
        #skip weekends
        if day.weekday() > 4:
            day += timedelta(days=1)
            continue

        for court in courts:
            for hour in range(start_hour, end_hour):
                dt = timezone.make_aware(datetime.combine(day, time(hour, 0)))
                #create new session, use get_or_create to avoid duplicates
                _, was_created = Session.objects.get_or_create(court=court,start_time=dt)
                if was_created:
                    created += 1

        day += timedelta(days=1)

    return created

