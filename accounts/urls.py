from django.urls import path
from . import views
from .views import signup
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("account/", views.account, name="account"),
    path("notifications/", views.notifications, name="notifications"),
    path("details/", views.my_details, name="details"),
]