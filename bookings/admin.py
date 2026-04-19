from django.contrib import admin
from .models import Court, Session, Booking, Comp_results

admin.site.register(Court)
admin.site.register(Session)
admin.site.register(Booking)

admin.site.register(Comp_results)