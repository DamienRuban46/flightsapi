from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
import datetime
from src.models import Flight, Seat, Reservation, Passenger
from src.serializers import FlightSerializer, SeatSerializer, ReservationSerializer, PassengerSerializer