from django.urls import path
from . import views

urlpatterns = [
    path("", views.staff_view, name="staff"),
    path("compresults/", views.comp_results, name="comp_results"),

]

