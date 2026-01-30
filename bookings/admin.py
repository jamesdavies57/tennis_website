from django.contrib import admin
from .models import Court, Session, Booking

admin.site.register(Court)
admin.site.register(Session)
admin.site.register(Booking)