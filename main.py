# Airtool 
# 62404051 | Muhammad Abdullah Farooqui
# BOCP Final Project 
"""
main.py - Entry point for AirTool application.
Console-based menu system for airport and flight management.
"""

from datetime import date

from airport import Airport
from flight import Flight
from file_manager import (
    initialize_data_files,
    read_airports_2d,
    read_flights_2d,
    load_airport_objects,
    load_flight_objects,
    write_booking,
    read_bookings,
    build_integrated_data,
)
from report_generator import (
    airport_traffic_report,
    flight_categorization_report,
    integrated_report,
    top_destinations_report,
    flight_trend_analysis,
    full_statistics_report,
    prompt_sort_option,
)
from utils import (
    APP_NAME,
    print_header,
    print_separator,
    get_valid_int,
    get_non_empty_string,
    pause,
)


def display_welcome():
    """Show application welcome banner."""
    print_header(APP_NAME)
    print("Welcome! Manage airports, flights, bookings, and analytics.\n")


def display_main_menu():
    """Display the main menu options."""
    print_header("MAIN MENU")
    print("  1.  View Airports")
    print("  2.  Search Airport")
    print("  3.  View Flights")
    print("  4.  Search Flight")
    print("  5.  Book Flight")
    print("  6.  Airport Traffic Report")
    print("  7.  Flight Trend Analysis")
    print("  8.  Top Destinations Report")
    print("  9.  View Saved Bookings")
    print(" 10.  Exit")
    print_separator()


def view_airports(airport_objects):
    """Option 1: Display all airports using OOP display_info()."""
    print_header("ALL AIRPORTS")
    if not airport_objects:
        print("No airports found.")
        return
    for index, airport in enumerate(airport_objects, start=1):
        print(f"\n[{index}] {airport.get_summary()}")
        airport.display_info()
    print()


def search_airport(airport_objects, airports_2d):
    """Option 2: Search airport by ID, name, or city."""
    print_header("SEARCH AIRPORT")
    print("Search by: 1=ID  2=Name  3=City")
    choice = input("Enter choice (1-3): ").strip()

    results = []
    if choice == "1":
        try:
            search_id = int(input("Enter Airport ID: "))
            for airport in airport_objects:
                if airport.airport_id == search_id:
                    results.append(airport)
        except ValueError:
            print("Error: Invalid airport ID. Please enter a number.")
            return
    elif choice == "2":
        keyword = input("Enter airport name (partial match): ").strip().lower()
        for airport in airport_objects:
            if keyword in airport.name.lower():
                results.append(airport)
    elif choice == "3":
        keyword = input("Enter city name (partial match): ").strip().lower()
        for airport in airport_objects:
            if keyword in airport.city.lower():
                results.append(airport)
    else:
        print("Error: Invalid search option.")
        return

    if results:
        print(f"\nFound {len(results)} airport(s):\n")
        for airport in results:
            airport.display_info()
            print()
    else:
        print("No matching airports found.")


def view_flights(flight_objects):
    """Option 3: Display all flights using OOP display_info()."""
    print_header("ALL FLIGHTS")
    if not flight_objects:
        print("No flights found.")
        return
    for index, flight in enumerate(flight_objects, start=1):
        print(f"\n[{index}] {flight.get_summary()}")
        flight.display_info()
    print()


def search_flight(flight_objects):
    """Option 4: Search flight by number or destination."""
    print_header("SEARCH FLIGHT")
    print("Search by: 1=Flight Number  2=Destination")
    choice = input("Enter choice (1-2): ").strip()

    results = []
    if choice == "1":
        keyword = input("Enter flight number: ").strip().upper()
        for flight in flight_objects:
            if flight.flight_number.upper() == keyword:
                results.append(flight)
    elif choice == "2":
        keyword = input("Enter destination (partial match): ").strip().lower()
        for flight in flight_objects:
            if keyword in flight.destination.lower():
                results.append(flight)
    else:
        print("Error: Invalid search option.")
        return

    if results:
        print(f"\nFound {len(results)} flight(s):\n")
        for flight in results:
            flight.display_info()
            print()
    else:
        print("No matching flights found.")


def book_flight(flight_objects):
    """Option 5: Book a flight and save to user_bookings.txt."""
    print_header("BOOK FLIGHT")
    if not flight_objects:
        print("No flights available to book.")
        return

    print("Available flights:")
    for flight in flight_objects:
        print(f"  {flight.flight_number} -> {flight.destination} ({flight.date})")

    flight_number = input("\nEnter flight number to book: ").strip().upper()
    selected_flight = None
    for flight in flight_objects:
        if flight.flight_number.upper() == flight_number:
            selected_flight = flight
            break

    if selected_flight is None:
        print(f"Error: Flight '{flight_number}' not found.")
        return

    passenger_name = get_non_empty_string("Enter passenger name: ")
    booking_date = input("Enter booking date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not booking_date:
        booking_date = str(date.today())

    print(f"\nBooking Summary:")
    print(f"  Passenger: {passenger_name}")
    selected_flight.display_info()
    print(f"  Booking Date: {booking_date}")

    confirm = input("\nConfirm booking? (y/n): ").strip().lower()
    if confirm == "y":
        if write_booking(passenger_name, selected_flight.flight_number, booking_date):
            print("\nBooking saved successfully to user_bookings.txt!")
        else:
            print("\nBooking could not be saved.")
    else:
        print("Booking cancelled.")


def view_bookings(flight_objects):
    """Option 9: Read and display saved bookings from file."""
    print_header("SAVED BOOKINGS")
    bookings = read_bookings()

    if not bookings:
        print("No bookings found.")
        return

    flight_lookup = {f.flight_number.upper(): f for f in flight_objects}
    print(f"{'Passenger':<20} {'Flight':<10} {'Destination':<15} {'Booking Date':<12}")
    print_separator("-")

    for booking in bookings:
        name, flight_num, book_date = booking[0], booking[1], booking[2]
        flight = flight_lookup.get(flight_num.upper())
        destination = flight.destination if flight else "Unknown"
        print(f"{name:<20} {flight_num:<10} {destination:<15} {book_date:<12}")
    print(f"\nTotal bookings: {len(bookings)}")


def show_integrated_with_sort(integrated_data):
    """Show integrated report with optional user-selected sorting."""
    sort_key, reverse = prompt_sort_option()
    if sort_key:
        from utils import sort_records
        records = sort_records(integrated_data, sort_key, reverse=reverse)
    else:
        records = integrated_data
    integrated_report(records)


def run_application():
    """Main application loop with menu handling and error handling."""
    initialize_data_files()

    # Load data into 2D lists (assignment requirement)
    airports_2d = read_airports_2d()
    flights_2d = read_flights_2d()

    # Load OOP objects from 2D data
    airport_objects = load_airport_objects(airports_2d)
    flight_objects = load_flight_objects(flights_2d)

    # Build integrated dataset by matching airport_id
    integrated_data = build_integrated_data(airports_2d, flights_2d)

    display_welcome()

    running = True
    while running:
        display_main_menu()

        try:
            choice = input("Enter your choice (1-10): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting AirTool. Goodbye!")
            break

        if choice == "1":
            view_airports(airport_objects)
            pause()

        elif choice == "2":
            search_airport(airport_objects, airports_2d)
            pause()

        elif choice == "3":
            view_flights(flight_objects)
            pause()

        elif choice == "4":
            search_flight(flight_objects)
            pause()

        elif choice == "5":
            book_flight(flight_objects)
            pause()

        elif choice == "6":
            airport_traffic_report(airports_2d, flights_2d)
            print("\n--- Flight Categories ---")
            flight_categorization_report(flights_2d)
            pause()

        elif choice == "7":
            bookings = read_bookings()
            flight_trend_analysis(flights_2d, bookings, integrated_data)
            full_statistics_report(airports_2d, flights_2d, bookings, integrated_data)
            pause()

        elif choice == "8":
            top_destinations_report(integrated_data)
            print("Integrated data (sortable):")
            show_integrated_with_sort(integrated_data)
            pause()

        elif choice == "9":
            view_bookings(flight_objects)
            pause()

        elif choice == "10":
            print_header("GOODBYE")
            print("Thank you for using AirTool. Safe travels!")
            running = False

        else:
            print("\nError: Invalid menu choice. Please enter a number from 1 to 10.")
            pause()


if __name__ == "__main__":
    run_application()
