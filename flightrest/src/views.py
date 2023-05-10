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
            return JsonResponse({"message" : "No flights found"}, status = 404)
        
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
def reserve_seat(request):
    print(request["passenger"])
    try:
        try:
            flightId = request.data["flightId"]
            flight = Flight.objects.get(flightId = flightId).data
        except:
            return JsonResponse({"message" : "Flight ID not found"})
        try:
            seatNumber = request.data["seatNumber"]
            seat = Seat.objects.get(flightId=flightId, seatNumber=seatNumber)
            if seat["taken"]:
                raise
            seatId = seat.seatId
            seat["taken"] = True
            seat.save()
        except:
            return JsonResponse({"message" : "Unable to reserve seat or does not exist"}, status = 404)
        try:
            passenger_data = request.data["passenger"]
            passenger_serializer = PassengerSerializer(data = passenger_data)
            if not passenger_serializer.is_valid():
                raise
            passenger = passenger_serializer.save()
        except:
            return JsonResponse({"message" : "Passenger details invalid"}, status = 400)
        try:
            reservation_data = {"seatId" : seatId,
                "passengerId" : passenger.passengerId,
                "holdingLuggage" : request.data["holdingLuggage"],
                "paymentConfirmed" : request.data["paymentConfirmed"]}
            reservation_serializer = ReservationSerializer(data = reservation_data)
            if not reservation_serializer.is_valid():
                raise
            reservation =  reservation_serializer.save()
        except:
            return JsonResponse({"message" : "Reservation data invalid"}, status = 400)
        response_data = reservation_data
        response_data["reservationId"] = reservation.reservationId
        response_data["flight"] = FlightSerializer(flight)
        return Response(response_data, status = 200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)
    
