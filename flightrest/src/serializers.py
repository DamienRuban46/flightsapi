from rest_framework import serializers
from src.models import Flight, Seat, Reservation, Passenger

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = {"flight_id", "plane_model", "number_of_seats",
                  "seats_per_row", "departure_time", "arrival_time",
                  "destination", "origin"}
        
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = {"seat_id", "seat_number",
                  "seat_price"}

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = {"reservation", "hold_luggage", "payment_confirmed"}

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = {"passenger_id", "first_name", "last_name",
                  "DOB", "passport_number", "address"}