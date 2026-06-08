# Airtool 
# 62404051 | Muhammad Abdullah Farooqui
# BOCP Final Project 
"""
flight.py - Flight class for AirTool application.
Represents a flight with departure and passenger details.
"""


class Flight:
    """Represents a flight in the AirTool system."""

    def __init__(self, flight_number, airport_id, destination, passengers, flight_type, date):
        """
        Initialize a Flight object.

        Args:
            flight_number: Unique flight identifier (e.g. PK101)
            airport_id: ID of the departure airport
            destination: Destination city/country
            passengers: Number of passengers on the flight
            flight_type: Domestic or International
            date: Flight date (YYYY-MM-DD)
        """
        self.flight_number = flight_number
        self.airport_id = airport_id
        self.destination = destination
        self.passengers = passengers
        self.flight_type = flight_type
        self.date = date

    def display_info(self):
        """Display formatted flight information to the console."""
        print(f"  Flight:      {self.flight_number}")
        print(f"  Airport ID:  {self.airport_id}")
        print(f"  Destination: {self.destination}")
        print(f"  Passengers:  {self.passengers}")
        print(f"  Type:        {self.flight_type}")
        print(f"  Date:        {self.date}")

    def get_summary(self):
        """Return a one-line summary string for the flight."""
        return (
            f"{self.flight_number} -> {self.destination} "
            f"({self.passengers} pax, {self.flight_type}, {self.date})"
        )

    @classmethod
    def from_row(cls, row):
        """
        Create a Flight object from a CSV row (list of strings).

        Args:
            row: [flight_number, airport_id, destination, passengers, flight_type, date]
        """
        try:
            passengers = int(row[3])
            if passengers < 0:
                raise ValueError(f"Invalid passenger count: {passengers}")
            airport_id = int(row[1])
        except ValueError as error:
            raise ValueError(f"Invalid flight data in row: {error}") from error

        return cls(
            flight_number=row[0].strip(),
            airport_id=airport_id,
            destination=row[2].strip(),
            passengers=passengers,
            flight_type=row[4].strip(),
            date=row[5].strip(),
        )

    def to_row(self):
        """Convert Flight object to a list for 2D storage."""
        return [
            self.flight_number,
            str(self.airport_id),
            self.destination,
            str(self.passengers),
            self.flight_type,
            self.date,
        ]
