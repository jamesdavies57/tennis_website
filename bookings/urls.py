from django.urls import path
from .views import session_list, book_session_page

urlpatterns = [
    path("sessions/", session_list, name="session_list"),
    path("sessions/<int:session_id>/book/", book_session_page, name="book_session_page"),
]