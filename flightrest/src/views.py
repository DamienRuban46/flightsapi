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
        flight_data = Flight.objects.filter(departureTime__date=departure_date,
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
            flight = Flight.objects.get(flightId = flightId)
        except:
            return JsonResponse({"message" : "Flight ID not found"}, status = 404)
        try:
            seatNumber = request.data["seatNumber"]
            seat = Seat.objects.get(flightId = flight, seatNumber = seatNumber)
            if seat.taken:
                raise
            seatId = seat.seatId
            seat.taken = True
        except Exception as e:
            print(e)
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
                "holdLuggage" : request.data["holdLuggage"],
                "paymentConfirmed" : request.data["paymentConfirmed"]}
            reservation_serializer = ReservationSerializer(data = reservation_data)
            if not reservation_serializer.is_valid():
                raise
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Reservation data invalid"}, status = 400)
        response_data = reservation_data
        reservation =  reservation_serializer.save()
        response_data["reservationId"] = reservation.reservationId
        response_data["flight"] = FlightSerializer(flight).data
        seat.save()
        return Response(response_data, status = 200)

    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)
    
@api_view(["GET"])
def query_reservation(request, reservationId):
    try:
        try:
            reservation_data = Reservation.objects.get(reservationId = reservationId)
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Reservation ID not found"}, status = 404)
        # passenger_data = Passenger.objects.get(passengerId = reservation_data["passengerId"])
        reservation_serialised = ReservationSerializer(reservation_data).data
        passenger_data = Passenger.objects.get(passengerId = reservation_serialised["passengerId"])
        passenger_serialised = PassengerSerializer(passenger_data).data
        # seat_data = Seat.objects.get(seatId = reservation_data["seatId"])
        seat_data = Seat.objects.get(seatId = reservation_serialised["seatId"])
        seat_serialised = SeatSerializer(seat_data).data
        print(seat_serialised)
        flight_data = Flight.objects.get(flightId = seat_serialised["flightId"])

        fligt_serialised = FlightSerializer(flight_data).data
        response_data = {"reservationId": reservationId,
                         "seat" : reservation_serialised["seatId"],
                         "holdLuggage" : reservation_serialised["holdLuggage"],
                         "paymentConfirmed" : reservation_serialised["paymentConfirmed"],
                         "passenger" : {"firstName" : passenger_serialised["firstName"],
                                        "lastName" : passenger_serialised["lastName"],
                                        "dateOfBirth" : passenger_serialised["dateOfBirth"],
                                        "passportNumber" : passenger_serialised["passportNumber"],
                                        "address" : passenger_serialised["address"]},
                         "flight" : {"flightId" : fligt_serialised["flightId"],
                                     "planeModel" : fligt_serialised["planeModel"],
                                     "numberOfRows" : fligt_serialised["numberOfRows"],
                                     "seatsPerRow" : fligt_serialised["seatsPerRow"],
                                     "departureTime" : fligt_serialised["departureTime"],
                                     "arrivalTime" : fligt_serialised["arrivalTime"],
                                     "departureAirport" : fligt_serialised["departureAirport"],
                                     "destinationAirport" : fligt_serialised["destinationAirport"]}}
        return Response(response_data, status = 200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)
    
@api_view(["PUT"])
def update_reservation(request, reservationId):
    try:
        try:
            reservation_data = Reservation.objects.get(reservationId = reservationId)
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Reservation ID not found"}, status = 404)
        try:
            holdLuggage = request.data["holdLuggage"]
            reservation_data.holdLuggage = holdLuggage
            reservation_data.save()
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Hold Luggage value invalid"})
        reservation_serialised = ReservationSerializer(reservation_data).data

        try:
            passenger_data = Passenger.objects.get(passengerId = reservation_serialised["passengerId"])
            for key, value in request.data["passenger"].items():
                passenger_data.key = value
            passenger_data.save()
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Invalid Value"})
        passenger_serialised = PassengerSerializer(passenger_data).data
        # seat_data = Seat.objects.get(seatId = reservation_serialised["seatId"])
        # seat_serialised = SeatSerializer(seat_data).data
        # flight_data = Flight.objects.get(flightId = seat_serialised["flightId"])
        response_data = {"reservationId": reservationId,
                         "seat" : reservation_serialised["seatId"],
                         "holdLuggage" : reservation_serialised["holdLuggage"],
                         "paymentConfirmed" : reservation_serialised["paymentConfirmed"],
                         "passenger" : {"firstName" : passenger_serialised["firstName"],
                                        "lastName" : passenger_serialised["lastName"],
                                        "dateOfBirth" : passenger_serialised["dateOfBirth"],
                                        "passportNumber" : passenger_serialised["passportNumber"],
                                        "address" : passenger_serialised["address"]},
                         "flight" : request.data["flight"]}
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
            reservation_data.paymentConfirmed = True
            reservation_data.save()
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Unable to confirm payment"}, status = 400)
        return Response(status = 200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Something went wrong please try again",}, status = 500)