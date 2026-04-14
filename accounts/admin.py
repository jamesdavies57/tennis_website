from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

@admin.register(Account)
class AccountAdmin(UserAdmin):
    model = Account
    ordering = ("email",)
    list_display = ("email", "username", "first_name", "last_name", "account_type", "is_staff")

    fieldsets = (
        ("Account", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "first_name", "last_name")}),
        ("Membership", {"fields": ("account_type", "membership_type", "membership_status", "competitive_rank", "unread_notifs")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "password1", "password2"),
        }),
    )