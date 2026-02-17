from django.urls import path
from . import views

urlpatterns = [
    path("", views.social_view, name="social"),
]