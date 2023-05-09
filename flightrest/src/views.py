from django.shortcuts import render
from rest_framework import viewsets

from src.models import Flight, Seat, Reservation, Passenger
from src.serializers import FlightSerializer, SeatSerializer, ReservationSerializer, PassengerSerializer

class FlightViewSet(viewsets.ModelViewSet):
    query = Flight.objects.all()
    serializer_class = FlightSerializer

class SeatViewSet(viewsets.ModelViewSet):
    query = Seat.objects.all()
    serializer_class = SeatSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    query = Reservation.objects.all()
    serializer_class = ReservationSerializer

class PassengerViewSet(viewsets.ModelViewSet):
    query = Passenger.objects.all()
    serializer_class = PassengerSerializer