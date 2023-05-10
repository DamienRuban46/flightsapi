from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import datetime
from src.models import Flight, Seat, Reservation, Passenger
from src.serializers import FlightSerializer, SeatSerializer, ReservationSerializer, PassengerSerializer
from django.core.serializers import serialize

@api_view(["GET"])
def query_flights(request, date, departureAirport, destinationAirport):
    try:
        if request.method != "GET":
            return JsonResponse({"message" : "Not get"}, status = 400) 
        
        try:
            departure_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return JsonResponse({"message" : "Invalid date format"}, status = 400)
        flight_data = Flight.objects.filter(departureTime__date=date,
                                        departureAirport=departureAirport,
                                        destinationAirport=destinationAirport)
        if not flight_data.exists():
            return JsonResponse({"message" : "No flights found"}, status=404)
        
        flight_serialised = FlightSerializer(flight_data, many = True).data

        response_data = []
        for flight in flight_serialised:
            response_data.append(flight)
            seat_data = Seat.objects.filter(flightId=flight["flightId"],
                                             taken=False)
            seats_serialised = SeatSerializer(seat_data, many = True).data
            response_data[-1]["seats"] = seats_serialised


        return Response(response_data, status = 200)        
        
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)
    
@api_view(["POST"])
def reserve_seats(request):
    try:
        
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)