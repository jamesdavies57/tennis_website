from django.urls import path
from . import views

urlpatterns = [
    path("", views.staff_view, name="staff"),
    path("compresults/", views.comp_results, name="comp_results"),
    path("usermanagement/", views.user_management, name="user_management"),
    path("manageauser<int:user_id>/", views.manage_a_user, name="manage_a_user"),
    path("announcements/", views.announcements, name="announcements"),
    path("staffsignup/", views.staff_signup, name="staff_signup"),
    path("staffmanagement/", views.staff_management, name="staff_management"),
    path("manageastaff<int:user_id>/", views.manage_a_staff, name="manage_a_staff"),
    path("generatesessions/", views.generate_sessions_view, name="generate_sessions"),
]

