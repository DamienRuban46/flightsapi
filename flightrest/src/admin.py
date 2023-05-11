from django.contrib import admin
from src.models import Flight, Seat, Reservation, Passenger

admin.site.register(Flight)
admin.site.register(Seat)
admin.site.register(Passenger)
admin.site.register(Reservation)