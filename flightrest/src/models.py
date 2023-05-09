from django.db import models

# Create your models here.
class Flight(models.Model):
    flight_id = models.UUIDField(primary_key=True)
    plane_model = models.CharField(max_length=100)
    number_of_rows = models.IntegerField()
    seats_per_row = models.SmallIntegerField()
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    destination = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)

class Seat(models.Model):
    seat_id = models.UUIDField(primary_key=True)
    flight_id = models.ForeignKey(Flight, on_delete=models.DO_NOTHING)
    seat_number = models.IntegerField()
    seat_price = models.FloatField()

class Passenger(models.Model):
    passenger_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    DOB = models.DateField()
    passport_number = models.IntegerField()
    address = models.CharField(max_length=100)

class Reservation(models.Model):
    reservation = models.IntegerField(primary_key=True)
    seat_id = models.ForeignKey(Seat, on_delete=models.DO_NOTHING)
    passenger_id = models.ForeignKey(Passenger, on_delete=models.DO_NOTHING)
    hold_luggage = models.BooleanField()
    payment_confirmed = models.BooleanField()

