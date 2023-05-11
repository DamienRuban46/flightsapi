from rest_framework import serializers
from src.models import Flight, Seat, Passenger, Reservation

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("flightId", "planeModel", "numberOfRows",
                  "seatsPerRow", "departureTime", "arrivalTime",
                  "departureAirport", "destinationAirport",)

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ("flightId", "seatNumber", "seatPrice",)

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("reservationId", "seatId", "passengerId", 
                  "holdLuggage", "paymentConfirmed",)

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("passengerId", "firstName", "lastName", 
                  "dateOfBirth", "passportNumber", "address",)