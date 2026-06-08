# Airtool 
# 62404051 | Muhammad Abdullah Farooqui
# BOCP Final Project 
"""
file_manager.py - File input/output operations for AirTool.
Handles reading CSV data, writing/reading bookings, and sample file creation.
"""

import os

from airport import Airport
from flight import Flight
from utils import AIRPORTS_FILE, FLIGHTS_FILE, BOOKINGS_FILE


# Sample data used when CSV files do not exist
SAMPLE_AIRPORTS = [
    "1,JFK Airport,USA,New York,8",
    "2,Heathrow,UK,London,5",
    "3,Dubai International,UAE,Dubai,3",
    "4,Changi Airport,Singapore,Singapore,4",
    "5,Sydney Airport,Australia,Sydney,3",
]

SAMPLE_FLIGHTS = [
    "PK101,1,Dubai,220,International,2025-10-01",
    "PK202,1,London,180,International,2025-10-05",
    "PK301,2,Paris,150,International,2025-10-02",
    "PK302,2,Frankfurt,95,International,2025-10-08",
    "PK401,3,Mumbai,310,International,2025-10-03",
    "PK402,3,Karachi,275,International,2025-10-12",
    "PK501,4,Bangkok,190,International,2025-10-04",
    "PK502,4,Tokyo,205,International,2025-10-15",
    "PK601,5,Melbourne,160,Domestic,2025-10-06",
    "PK602,5,Brisbane,140,Domestic,2025-10-10",
    "PK103,1,Chicago,130,Domestic,2025-11-01",
    "PK203,1,Miami,145,Domestic,2025-11-05",
    "PK303,2,Manchester,88,Domestic,2025-11-02",
    "PK403,3,Riyadh,200,International,2025-11-03",
    "PK503,4,Hong Kong,230,International,2025-11-04",
]


def create_sample_file(filepath, lines):
    """Write sample lines to a file if it does not exist."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")
        print(f"Sample file created: {filepath}")
    except IOError as error:
        print(f"Error creating sample file {filepath}: {error}")


def initialize_data_files():
    """Create sample CSV files if they are missing."""
    if not os.path.exists(AIRPORTS_FILE):
        create_sample_file(AIRPORTS_FILE, SAMPLE_AIRPORTS)
    if not os.path.exists(FLIGHTS_FILE):
        create_sample_file(FLIGHTS_FILE, SAMPLE_FLIGHTS)
    if not os.path.exists(BOOKINGS_FILE):
        try:
            with open(BOOKINGS_FILE, "w", encoding="utf-8") as file:
                file.write("# Passenger Name | Flight Number | Booking Date\n")
        except IOError as error:
            print(f"Error creating bookings file: {error}")


def read_airports_2d():
    """
    Read airports from CSV and return as a 2D list.
    Each inner list: [id, name, country, city, terminal_count]
    """
    airports_2d = []
    try:
        with open(AIRPORTS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                row = [part.strip() for part in line.split(",")]
                if len(row) >= 5:
                    airports_2d.append(row)
    except FileNotFoundError:
        print(f"Error: File '{AIRPORTS_FILE}' not found. Creating sample data...")
        create_sample_file(AIRPORTS_FILE, SAMPLE_AIRPORTS)
        return read_airports_2d()
    except IOError as error:
        print(f"Error reading airports file: {error}")
    return airports_2d


def read_flights_2d():
    """
    Read flights from CSV and return as a 2D list.
    Each inner list: [flight_no, airport_id, destination, passengers, type, date]
    """
    flights_2d = []
    try:
        with open(FLIGHTS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                row = [part.strip() for part in line.split(",")]
                if len(row) >= 6:
                    flights_2d.append(row)
    except FileNotFoundError:
        print(f"Error: File '{FLIGHTS_FILE}' not found. Creating sample data...")
        create_sample_file(FLIGHTS_FILE, SAMPLE_FLIGHTS)
        return read_flights_2d()
    except IOError as error:
        print(f"Error reading flights file: {error}")
    return flights_2d


def load_airport_objects(airports_2d):
    """Convert 2D airport list into a list of Airport objects."""
    airport_objects = []
    for row in airports_2d:
        try:
            airport_objects.append(Airport.from_row(row))
        except (ValueError, IndexError) as error:
            print(f"Warning: Skipping invalid airport row {row}: {error}")
    return airport_objects


def load_flight_objects(flights_2d):
    """Convert 2D flight list into a list of Flight objects."""
    flight_objects = []
    for row in flights_2d:
        try:
            flight_objects.append(Flight.from_row(row))
        except (ValueError, IndexError) as error:
            print(f"Warning: Skipping invalid flight row {row}: {error}")
    return flight_objects


def write_booking(passenger_name, flight_number, booking_date):
    """
    Append a booking record to user_bookings.txt.

    Args:
        passenger_name: Name of the passenger
        flight_number: Booked flight number
        booking_date: Date of booking (YYYY-MM-DD)
    """
    try:
        with open(BOOKINGS_FILE, "a", encoding="utf-8") as file:
            file.write(f"{passenger_name},{flight_number},{booking_date}\n")
        return True
    except IOError as error:
        print(f"Error writing booking: {error}")
        return False


def read_bookings():
    """
    Read all bookings from user_bookings.txt.
    Returns list of [passenger_name, flight_number, booking_date].
    """
    bookings = []
    try:
        with open(BOOKINGS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 3:
                    bookings.append(parts[:3])
    except FileNotFoundError:
        print(f"Note: No bookings file found at '{BOOKINGS_FILE}'.")
    except IOError as error:
        print(f"Error reading bookings: {error}")
    return bookings


def build_integrated_data(airports_2d, flights_2d):
    """
    Combine airports and flights by matching airport_id.
    Returns list of dicts with airport_name, city, destination, passengers, etc.
    """
    integrated = []
    airport_lookup = {}
    for row in airports_2d:
        try:
            airport_lookup[int(row[0])] = {
                "name": row[1],
                "city": row[3],
                "country": row[2],
            }
        except (ValueError, IndexError):
            continue

    for flight_row in flights_2d:
        try:
            airport_id = int(flight_row[1])
            info = airport_lookup.get(airport_id, {"name": "Unknown", "city": "Unknown", "country": "Unknown"})
            integrated.append({
                "flight_number": flight_row[0],
                "airport_id": airport_id,
                "airport_name": info["name"],
                "city": info["city"],
                "country": info["country"],
                "destination": flight_row[2],
                "passengers": int(flight_row[3]),
                "flight_type": flight_row[4],
                "date": flight_row[5],
            })
        except (ValueError, IndexError) as error:
            print(f"Warning: Skipping invalid flight for integration: {error}")
    return integrated
