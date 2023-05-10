from io import StringIO
from typing import Optional
from django.core.management.base import BaseCommand
from src.models import Flight, Seat
from datetime import date, datetime, timedelta, time
import random
import sqlite3



class Command(BaseCommand):

    def handle(self, *args, **options):
        self.view_flights()
        self.view_seats()

    def view_flights(self):
        values = Flight.objects.all().values()
        for value in values:
            self.stdout.write(self.style.SUCCESS(value))
        self.stdout.write(self.style.SUCCESS("Success"))

    def view_seats(self):
        values = Seat.objects.all().values()
        for value in values[197:200]:
            self.stdout.write(self.style.SUCCESS(value))

        self.stdout.write(self.style.SUCCESS("Success"))