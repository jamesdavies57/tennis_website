from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Court(models.Model):
    COURT_TYPES = (
        ("CASUAL", "Casual"),
        ("COMPETITIVE", "Competitive"),
    )

    name = models.CharField(max_length=50, unique=True)
    court_type = models.CharField(max_length=15, choices=COURT_TYPES, default=("CASUAL","Casual"))
    max_players = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Session(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="sessions")
    start_time = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)

    #using properties allows data to be called later without being stored
    @property
    def end_time(self):
        return self.start_time + timedelta(hours=1)

    @property
    def session_type(self):
        return self.court.court_type

    @property
    def max_players(self):
        return self.court.max_players

    class Meta:
        #add constraint to make sure a court cannot have multiple sessions at the same time
        constraints = [models.UniqueConstraint(fields=["court", "start_time"], name="unique_court_start"),]
        ordering = ["start_time"]


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="bookings")

    date_created = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    #is_cancelled can be called later to find if session has been cancelled 
    @property
    def is_cancelled(self):
        return self.cancelled_at is not None

    #make sure user can only book session once
    class Meta:
        unique_together = ("user", "session")

    def __str__(self):
        return f"{self.user.email}: {self.session}"
