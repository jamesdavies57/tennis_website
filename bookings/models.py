from django.db import models
from django.conf import settings
from datetime import timedelta
from accounts.models import Account
from django.utils import timezone

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

    @property
    def end_time(self):
        return self.start_time + timedelta(hours=1)

    @property
    def session_type(self):
        return self.court.court_type

    @property
    def max_players(self):
        return self.court.max_players
    
    def __str__(self):
        bookings = self.bookings.all()

        if not bookings.exists():
            players = "No players"
        else:
            players = ", ".join([b.user.email for b in bookings])

        return f"{self.court}: {self.start_time.strftime('%d %b %Y %H:%M')} - {players}"

    class Meta:
        #add constraint to make sure a court cannot have multiple sessions at the same time
        constraints = [models.UniqueConstraint(fields=["court", "start_time"], name="unique_court_start"),]
        ordering = ["start_time"]


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="bookings")

    date_created = models.DateTimeField(default=timezone.now)
    cancelled_at = models.DateTimeField(null=True, blank=True)
     
    @property
    def is_cancelled(self):
        return self.cancelled_at is not None

    #make sure user can only book session once
    class Meta:
        unique_together = ("user", "session")

    def __str__(self):
        return f"{self.user.email}: {self.session}"

class Comp_results(models.Model):

    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name="results", null=True, blank=True)

    player1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comp_player_1")
    player2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comp_player_2")

    #results for each player in each set in the match
    p1s1 = models.IntegerField()
    p1s2 = models.IntegerField()
    p1s3 = models.IntegerField(null=True, blank=True)

    p2s1 = models.IntegerField()
    p2s2 = models.IntegerField()
    p2s3 = models.IntegerField(null=True, blank=True)

    time = models.DateTimeField(default=timezone.now)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comp_recording")

    p1_elo_change = models.IntegerField(null=True, blank=True)
    p2_elo_change = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["session"],name="one_result_per_session")]

    def __str__(self):
        return f"{self.session.court} {self.session.start_time}: {self.player1.email} vs {self.player2.email}"
    
    
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        #only update ranks the first time the match is recorded
        if is_new:
            self.update_ranks()

    def get_winner(self):
        p1_sets = 0
        p2_sets = 0
        #count sets won, skip if set wasnt played
        if self.p1s1 > self.p2s1:
            p1_sets += 1
        else:
            p2_sets += 1
        if self.p1s2 > self.p2s2:
            p1_sets += 1
        else:
            p2_sets += 1
        if self.p1s3 is not None and self.p2s3 is not None:
            if self.p1s3 > self.p2s3:
                p1_sets += 1
            else:
                p2_sets += 1
        return p1_sets, p2_sets


    #calculate elo and update
    def update_ranks(self):
        p1 = self.player1
        p2 = self.player2
        p1_sets, p2_sets = self.get_winner()

        if p1_sets == p2_sets:
            return

        #work out who won
        if p1_sets > p2_sets:
            p1_win, p2_win = 1, 0
        else:
            p1_win, p2_win = 0, 1

        r1 = p1.competitive_rank
        r2 = p2.competitive_rank

        #calculate how likely each player was to win based on rank difference
        p1_expected = 1 / (1 + 10 ** ((r2 - r1) / 400))
        p2_expected = 1 / (1 + 10 ** ((r1 - r2) / 400))

        #update ranks
        new_r1 = r1 + 32 * (p1_win - p1_expected)
        new_r2 = r2 + 32 * (p2_win - p2_expected)

        self.p1_elo_change = round(new_r1 - r1)
        self.p2_elo_change = round(new_r2 - r2)
        self.save(update_fields=["p1_elo_change", "p2_elo_change"])

        p1.competitive_rank = round(new_r1)
        p2.competitive_rank = round(new_r2)
        p1.save()
        p2.save()