from io import StringIO
from typing import Optional
from django.core.management.base import BaseCommand
from src.models import Flight, Seat
from datetime import date, datetime, timedelta, time
import random



class Command(BaseCommand):

    def handle(self, *args, **options):
        self.flights = []
        self.journeys = [{"airport 1" : "LBA",
                           "airport 2" : "BHD",
                           "duration" : 1,
                           "cost" : 50},
                            {"airport 1" : "LBA",
                             "airport 2" : "DXB",
                             "duration" : 10,
                             "cost" : 300}, 
                            {"airport 1" : "IPC",
                             "airport 2" : "DXB",
                             "duration" : 10,
                             "cost" : 300}, 
                            {"airport 1" : "CCU",
                             "airport 2" : "DXB",
                             "duration" : 10,
                             "cost" : 220},
                            {"airport 1" : "SYD",
                             "airport 2" : "DXB",
                             "duration" : 10,
                             "cost" : 800},
                            {"airport 1" : "SYD",
                             "airport 2" : "CCU",
                             "duration" : 10,
                             "cost" : 500},]
        self.aircraft = [{"model" : "Airbus 320",
                          "no of rows": 33,
                          "row width" : 6,
                          "no of seats" : 198}, 
                          {"model" : "Boeing 737",
                           "no of rows" : 33,
                           "row width" : 6,
                           "no of seats" : 198}, 
                          {"model" : "Boeing 757",
                           "no of rows" : 50,
                           "row width" : 6,
                           "no of seats" : 300}]
        self.add_flights(2)

        self.stdout.write(self.style.SUCCESS("Success"))


    def add_flights(self, amount):
        Flight.objects.all().delete()
        Seat.objects.all().delete()
        flight_date = date.today()#tz=get_current_timezone())
        for _ in range (10):
            for i in range (amount):
                for journey in self.journeys:
                    dt = datetime.combine(flight_date, time.min)
                    dt = datetime.combine(dt, time(hour=random.randint(0,23))) # Random amount
                    #Randomly select an aircraft
                    #Need to calculate distance between them
                    aircraft_index = random.randint(0,2)
                    flight_info = {"plane_model" : self.aircraft[aircraft_index]["model"],
                                "number_of_rows" : self.aircraft[aircraft_index]["no of rows"],
                                "seats_per_row": self.aircraft[aircraft_index]["row width"],
                                "origin" : journey["airport 1"],
                                "destination" : journey["airport 2"],
                                "departure_time" : dt,
                                "arrival_time" : datetime.combine(dt, time(hour=journey["duration"]))}
                    
                    flight = Flight.objects.create(**flight_info)
                    for seat_no in range(self.aircraft[aircraft_index]["no of seats"]):
                        seat = {"flight_id" : flight,
                                "seat_number" : seat_no + 1,
                                "seat_price" : 100,
                                "booked" : False}
                        Seat.objects.create(**seat)

                    flight_info = {"plane_model" : self.aircraft[aircraft_index]["model"],
                                "number_of_rows" : self.aircraft[aircraft_index]["no of rows"],
                                "seats_per_row": self.aircraft[aircraft_index]["row width"],
                                "origin" : journey["airport 2"],
                                "destination" : journey["airport 1"],
                                "departure_time" : dt,
                                "arrival_time" : datetime.combine(dt, time(hour=journey["duration"]))}
                    
                    flight = Flight.objects.create(**flight_info)
                    for seat_no in range(self.aircraft[aircraft_index]["no of seats"]):
                        seat = {"flight_id" : flight,
                                "seat_number" : seat_no + 1,
                                "seat_price" : 100,
                                "booked" : False}
                        Seat.objects.create(**seat)

            flight_date += timedelta(days=1)
            self.stdout.write(self.style.SUCCESS(_/30))

