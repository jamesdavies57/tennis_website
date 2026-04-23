from django.urls import path
from . import views

urlpatterns = [
    path("", views.staff_view, name="staff"),
    path("compresults/", views.comp_results, name="comp_results"),
    path("usermanagement/", views.user_management, name="user_management"),
    path("manageauser<int:user_id>/", views.manage_a_user, name="manage_a_user"),
]

