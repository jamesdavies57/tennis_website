from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, time, timedelta
from bookings.models import Court, Session
from django.db import transaction

class Command(BaseCommand):
    help = "Generate court sessions from specified date."

    def add_arguments(self, parser):
        parser.add_argument("--weeks", type=int, default=4)
        parser.add_argument("--start-hour", type=int, default=9)
        parser.add_argument("--end-hour", type=int, default=21)
        parser.add_argument("--start-date",type=str,help="YYYY-MM-DD",)

    @transaction.atomic
    def handle(self, *args, **opts):
        weeks = opts["weeks"]
        start_hour = opts["start_hour"]
        end_hour = opts["end_hour"]

        start_date_str = opts.get("start_date")

        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        else:
            start_date = timezone.localtime().date()
        end_date = start_date + timedelta(weeks=weeks)

        courts = Court.objects.filter(is_active=True)
        created = 0

        day = start_date
        while day < end_date:
            weekday = day.weekday() 

            #only create sessions for weekdays
            if weekday > 4:
                day += timedelta(days=1)
                continue

            for court in courts:
                for hour in range(start_hour, end_hour):
                    dt = timezone.make_aware(datetime.combine(day, time(hour, 0)))

                    obj, was_created = Session.objects.get_or_create(
                        court=court,
                        start_time=dt,
                        defaults={"is_cancelled": False},
                    )
                    if was_created:
                        created += 1

            day += timedelta(days=1)


        self.stdout.write(self.style.SUCCESS(f"Created {created} sessions."))