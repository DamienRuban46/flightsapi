from django.db import models

class Flight(models.Model):
    flightId = models.AutoField(primary_key=True)
    planeModel = models.CharField(max_length=20)
    numberOfRows = models.IntegerField()
    seatsPerRow = models.IntegerField()
    departureTime = models.DateTimeField()
    arrivalTime = models.DateTimeField()
    departureAirport = models.CharField(max_length=100)
    destinationAirport = models.CharField(max_length=100)

class Seat(models.Model):
    seatId = models.AutoField(primary_key=True)
    flightId = models.ForeignKey(Flight, on_delete=models.DO_NOTHING,)
    seatNumber = models.IntegerField()
    seatPrice = models.DecimalField(decimal_places=2, max_digits=10)
    taken = models.BooleanField()


class Passenger(models.Model):
    passengerId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    dateOfBirth = models.DateField()
    passportNumber = models.IntegerField()
    address = models.CharField(max_length=200)

class Reservation(models.Model):
    reservationId = models.AutoField(primary_key=True)
    seatId = models.ForeignKey(Seat, on_delete=models.DO_NOTHING,)
    passengerId = models.ForeignKey(Passenger, on_delete=models.DO_NOTHING,)
    holdLuggage = models.BooleanField()
    paymentConfirmed = models.BooleanField()