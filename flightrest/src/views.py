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
    try:
        try:
            flightId = request.data["flightId"]
            flight = Flight.objects.get(flightId = flightId).data
        except:
            return JsonResponse({"message" : "Flight ID not found"})
        try:
            seatNumber = request.data["seatNumber"]
            seat = Seat.objects.get(flightId = flightId, seatNumber = seatNumber)
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
    
@api_view(["POST"])
def query_reservation(request, reservationId):
    try:
        try:
            reservation_data = Reservation.objects.get(reservationId = reservationId)
        except:
            return JsonResponse({"message" : "Reservation ID not found"}, status = 404)
        passenger_data = Passenger.objects.get(passengerId = reservation_data["passengerId"])
        # reservation_serialised = ReservationSerializer(reservation).data
        # passenger_data = Passenger.objects.get(passengerId = reservation_serialised["passengerId"])
        # passenger_serialised = PassengerSerializer(passenger_data).data
        seat_data = Seat.objects.get(seatId = reservation_data["seatId"])
        # seat_data = Seat.objects.get(seatId = reservation_serialised["seatId"])
        flight_data = Flight.objects.get(flightId = seat_data["flightId"])
        response_data = {"reservationId": reservationId,
                         "seat" : reservation_data["seatId"],
                         "holdLuggage" : reservation_data["holdLuggage"],
                         "paymentConfirmed" : reservation_data["paymentConfirmed"],
                         "passenger" : {"firstName" : passenger_data["firstName"],
                                        "lastName" : passenger_data["lastName"],
                                        "dateOfBirth" : passenger_data["dateOfBirth"],
                                        "passportNumber" : passenger_data["passportNumber"],
                                        "address" : passenger_data["address"]},
                         "flight" : {"flightId" : flight_data["flightId"],
                                     "planeModel" : flight_data["planeModel"],
                                     "numberOfRows" : flight_data["numberOfRows"],
                                     "seatsPerRow" : flight_data["seatsPerRow"],
                                     "departureTime" : flight_data["departureTime"],
                                     "arrivalTime" : flight_data["arrivalTime"],
                                     "departureAirport" : flight_data["departureAirport"],
                                     "destinationAirport" : flight_data["destinationAirport"]}}
        return Response(response_data, status = 200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)
    
@api_view(["PUT"])
def update_reservation(request, reservationId):
    try:
        try:
            reservation_data = Reservation.objects.get(reservationId = reservationId)
        except:
            return JsonResponse({"message" : "Reservation ID not found"}, status = 404)
        try:
            holdLuggage = request.data["holdLuggage"]
            reservation_data["holdLuggage"] = holdLuggage
            reservation_data.save()
        except:
            return JsonResponse({"message" : "Hold Luggage value invalid"})
        try:
            passenger_data = Passenger.objects.get(passengerId = request.data["passenger"])
            for key, value in passenger_data.items():
                passenger_data[key] = value
            passenger_data.save()
        except:
            return JsonResponse({"message" : "Invalid Value"})
        seat_data = Seat.objects.get(seatId = reservation_data["seatId"])
        flight_data = Flight.objects.get(flightId = seat_data["flightId"])
        response_data = {"reservationId": reservationId,
                         "seat" : reservation_data["seatId"],
                         "holdLuggage" : reservation_data["holdLuggage"],
                         "paymentConfirmed" : reservation_data["paymentConfirmed"],
                         "passenger" : {"firstName" : passenger_data["firstName"],
                                        "lastName" : passenger_data["lastName"],
                                        "dateOfBirth" : passenger_data["dateOfBirth"],
                                        "passportNumber" : passenger_data["passportNumber"],
                                        "address" : passenger_data["address"]},
                         "flight" : {"flightId" : flight_data["flightId"],
                                     "planeModel" : flight_data["planeModel"],
                                     "numberOfRows" : flight_data["numberOfRows"],
                                     "seatsPerRow" : flight_data["seatsPerRow"],
                                     "departureTime" : flight_data["departureTime"],
                                     "arrivalTime" : flight_data["arrivalTime"],
                                     "departureAirport" : flight_data["departureAirport"],
                                     "destinationAirport" : flight_data["destinationAirport"]}}
        return Response(response_data, status = 200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)
    
@api_view(["DELETE"])
def delete_reservation(request, reservationId):
    try:
        try:
            reservation_data = Reservation.objects.get(reservationId = reservationId)
            reservation_data.delete()
            return Response(status = 200)
        except:
            return JsonResponse({"message" : "Reservation ID not found"}, status = 404)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)

@api_view(["PUT"])
def confirm_reservation(request, reservationId):    
    try:
        try:
            reservation_data = Reservation.objects.get(reservationId = reservationId)
        except:
            return JsonResponse({"message" : "Reservation ID not found"}, status = 404)
        try:
            reservation_data["paymentConfirmed"] = True
            reservation_data.save()
        except:
            return JsonResponse({"message" : "Unable to confirm payment"})
        return Response(status = 200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)