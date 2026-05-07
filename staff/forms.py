from django import forms
from bookings.models import Comp_results, Session
from accounts.models import Account
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm

class CompForm(forms.ModelForm):
    session = forms.ModelChoiceField(
        queryset=Session.objects.filter(
            court__court_type="COMPETITIVE",
            is_cancelled=False,
            start_time__gte=timezone.now()
        ),
        label="Match (Date & Time)"
    )

    class Meta:
        model = Comp_results
        fields = [
            "session",
            "p1s1", "p2s1",
            "p1s2", "p2s2",
            "p1s3", "p2s3",
        ]
    def clean_session(self):
        session = self.cleaned_data.get("session")

        if session and hasattr(session, "result"):
            raise forms.ValidationError("A result already exists for this session.")

        return session
    
class StaffCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.competitive_rank = 1000
        user.membership_type = "PREMIUM"
        user.account_type = "STAFF"
        user.is_staff = True
        user.is_superuser = False

        if commit:
            user.save()

        return user