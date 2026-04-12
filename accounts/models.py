from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager,)
from django.utils import timezone
from django.conf import settings


class AccountManager(BaseUserManager):
    #creating a user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not extra_fields.get("username"):
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #creating a superuser
    def create_superuser(self, email, password=None, **extra_fields): 
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("account_type", "STAFF")

        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_TYPES = [
        ("MEMBER", "Member"),
        ("STAFF", "Staff"),
    ]

    MEMBERSHIP_STATUS = [
        ("ACTIVE", "Active"),
        ("PAUSED", "Paused"),
        ("CANCELLED", "Cancelled"),
    ]

    MEMBERSHIP_TYPES = [
        ("CASUAL", "Casual"),
        ("PREMIUM", "Premium"),
    ]

    #Fields
    id = models.BigAutoField(primary_key=True)

    email = models.EmailField(unique=True)

    username = models.CharField(max_length=30, unique=True)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    #Set account classification
    account_type = models.CharField(max_length=10,choices=ACCOUNT_TYPES,default="MEMBER",)

    #Membership info (can be blank for staff)
    membership_type = models.CharField(max_length=20,choices=MEMBERSHIP_TYPES,null=True,blank=True,)

    membership_status = models.CharField(max_length=20,choices=MEMBERSHIP_STATUS,null=True,blank=True,)

    competitive_rank = models.PositiveIntegerField(null=True,blank=True,)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = AccountManager()

    #set username to email as login, despite having a username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.username
    

class Notification(models.Model):
    NOTIF_TYPES = (
        ("BOOKING", "Booking"),
        ("SOCIAL", "Social"),
        ("ACCOUNT","Account"),
        ("STAFF","Staff"),
        ("ANNOUNCEMENT","Announcement"),
        ("WARNING","Warning"),
        ("OTHER","Other"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification")
    notif_type = models.CharField(max_length=15, choices=NOTIF_TYPES, default="OTHER")
    title = models.CharField(max_length = 50)
    body = models.CharField(max_length = 500)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title