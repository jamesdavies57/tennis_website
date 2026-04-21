from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name", "membership_type")

    def save(self, commit=True):
        #if user makes a premium account, set their rank to 100 to start
        user = super().save(commit=False)

        if user.membership_type == "PREMIUM":
            user.competitive_rank = 1000

        if commit:
            user.save()

        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["username", "email", "membership_type"] 

    def save(self, commit=True):
        #if user has no rank already, make it 100, if not use their old value
        user = super().save(commit=False)

        if user.membership_type == "PREMIUM" and not user.competitive_rank:
            user.competitive_rank = 1000

        if commit:
            user.save()

        return user