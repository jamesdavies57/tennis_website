from django import forms
from bookings.models import Comp_results, Session
from django.utils import timezone
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