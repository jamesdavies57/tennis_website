from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name", "membership_type")