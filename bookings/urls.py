from django.urls import path
from .views import casual_sessions, competitive_sessions, my_bookings, cancel_my_booking, book_session_page

urlpatterns = [
    path("casual/", casual_sessions, name="casual_sessions"),
    path("competitive/", competitive_sessions, name="competitive_sessions"),

    path("sessions/<int:session_id>/book/", book_session_page, name="book_session_page"),

    path("mine/", my_bookings, name="my_bookings"),
    path("mine/<int:booking_id>/cancel/", cancel_my_booking, name="cancel_my_booking"),
]