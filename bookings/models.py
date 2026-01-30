from django.db import models
from django.conf import settings

class Court(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Session(models.Model):
    SESSION_TYPE_CHOICES = (
        ("CASUAL", "Casual"),
        ("COMPETITIVE", "Competitive"),
    )

    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="sessions")

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    max_players = models.PositiveSmallIntegerField(default=2)

    session_type = models.CharField(max_length=15, choices=SESSION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.court.name} | {self.start_time}"
    

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="bookings")

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "session")

    def __str__(self):
        return f"{self.user.email}: {self.session}"
