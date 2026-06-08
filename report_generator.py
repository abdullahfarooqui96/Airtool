# Airtool 
# 62404051 | Muhammad Abdullah Farooqui
# BOCP Final Project 
"""
report_generator.py - Report generation for AirTool.
Generates traffic reports, trend analysis, and destination rankings.
Uses nested loops where required by assignment specification.
"""

from collections import defaultdict

from utils import (
    print_header,
    print_separator,
    categorize_flights,
    parse_month,
    sort_records,
    SORT_BY_PASSENGERS,
    SORT_BY_AIRPORT,
    SORT_BY_DESTINATION,
    FLIGHT_DOMESTIC,
    FLIGHT_INTERNATIONAL,
)


def get_airport_name_by_id(airports_2d, airport_id):
    """Look up airport name from 2D airport list by ID."""
    for row in airports_2d:
        try:
            if int(row[0]) == airport_id:
                return row[1]
        except (ValueError, IndexError):
            continue
    return "Unknown Airport"


def airport_traffic_report(airports_2d, flights_2d):
    """
    Generate Airport Traffic Report using nested loops.
    Shows each airport and all flights departing from it.
    """
    print_header("AIRPORT TRAFFIC REPORT")
    print("Flights grouped by departure airport:\n")

    if not airports_2d:
        print("No airport data available.")
        return

    # Outer loop: iterate through each airport
    for airport_row in airports_2d:
        try:
            airport_id = int(airport_row[0])
            airport_name = airport_row[1]
            city = airport_row[3]
        except (ValueError, IndexError):
            continue

        print(f"{airport_name} ({city})")
        flight_found = False

        # Inner loop: find all flights for this airport
        for flight_row in flights_2d:
            try:
                if int(flight_row[1]) == airport_id:
                    flight_num = flight_row[0]
                    destination = flight_row[2]
                    passengers = flight_row[3]
                    print(f"  {flight_num} -> {destination} ({passengers} passengers)")
                    flight_found = True
            except (ValueError, IndexError):
                continue

        if not flight_found:
            print("  (No flights recorded)")
        print()


def flight_categorization_report(flights_2d):
    """Display flights grouped by Domestic and International categories."""
    print_header("FLIGHT CATEGORIZATION REPORT")
    categories = categorize_flights(flights_2d)

    for category_name in [FLIGHT_DOMESTIC, FLIGHT_INTERNATIONAL]:
        print(f"\n--- {category_name} Flights ---")
        flights_in_category = categories.get(category_name, [])
        if not flights_in_category:
            print("  None")
            continue
        for row in flights_in_category:
            print(f"  {row[0]} -> {row[2]} ({row[3]} passengers, {row[5]})")
    print()


def integrated_report(integrated_data, sort_key=None):
    """
    Show integrated report: Airport Name, City, Destination, Passenger Count.
    Optional sorting by passengers, airport name, or destination.
    """
    print_header("INTEGRATED AIRPORT-FLIGHT REPORT")
    print(f"{'Airport':<22} {'City':<14} {'Destination':<14} {'Passengers':<10}")
    print_separator()

    records = integrated_data
    if sort_key:
        records = sort_records(integrated_data, sort_key)

    for record in records:
        print(
            f"{record['airport_name']:<22} "
            f"{record['city']:<14} "
            f"{record['destination']:<14} "
            f"{record['passengers']:<10}"
        )
    print()


def top_destinations_report(integrated_data, top_n=5):
    """Report top destinations by total passenger count."""
    print_header("TOP DESTINATIONS REPORT")

    destination_totals = defaultdict(int)
    destination_flights = defaultdict(int)

    for record in integrated_data:
        dest = record["destination"]
        destination_totals[dest] += record["passengers"]
        destination_flights[dest] += 1

    if not destination_totals:
        print("No flight data available.")
        return

    sorted_destinations = sorted(
        destination_totals.items(), key=lambda item: item[1], reverse=True
    )

    print(f"{'Rank':<6} {'Destination':<18} {'Total Passengers':<18} {'Flights':<8}")
    print_separator()

    rank = 1
    for dest, total_pax in sorted_destinations[:top_n]:
        print(f"{rank:<6} {dest:<18} {total_pax:<18} {destination_flights[dest]:<8}")
        rank += 1

    print(f"\nMost popular destination: {sorted_destinations[0][0]} "
          f"({sorted_destinations[0][1]} total passengers)")
    print()


def flight_trend_analysis(flights_2d, bookings, integrated_data):
    """
    Analyze two trends:
    1. Passenger traffic over time (by month)
    2. Number of bookings over time (by month)
    """
    print_header("FLIGHT TREND ANALYSIS")

    # Trend 1: Monthly passenger traffic
    monthly_passengers = defaultdict(int)
    monthly_flight_count = defaultdict(int)

    for row in flights_2d:
        try:
            month = parse_month(row[5])
            passengers = int(row[3])
            monthly_passengers[month] += passengers
            monthly_flight_count[month] += 1
        except (ValueError, IndexError):
            continue

    print("\n--- Passenger Traffic Over Time (by Month) ---")
    if monthly_passengers:
        sorted_months = sorted(monthly_passengers.keys())
        print(f"{'Month':<12} {'Total Passengers':<18} {'Flights':<10}")
        print_separator("-")

        previous_pax = None
        for month in sorted_months:
            pax = monthly_passengers[month]
            flights = monthly_flight_count[month]
            growth_str = ""
            if previous_pax is not None and previous_pax > 0:
                growth = ((pax - previous_pax) / previous_pax) * 100
                growth_str = f"  (Growth: {growth:+.1f}%)"
            print(f"{month:<12} {pax:<18} {flights:<10}{growth_str}")
            previous_pax = pax
    else:
        print("  No passenger data available.")

    # Trend 2: Monthly booking counts
    monthly_bookings = defaultdict(int)
    for booking in bookings:
        if len(booking) >= 3:
            month = parse_month(booking[2])
            monthly_bookings[month] += 1

    print("\n--- Bookings Over Time (by Month) ---")
    if monthly_bookings:
        sorted_booking_months = sorted(monthly_bookings.keys())
        print(f"{'Month':<12} {'Bookings':<12}")
        print_separator("-")

        previous_bookings = None
        for month in sorted_booking_months:
            count = monthly_bookings[month]
            growth_str = ""
            if previous_bookings is not None and previous_bookings > 0:
                growth = ((count - previous_bookings) / previous_bookings) * 100
                growth_str = f"  (Growth: {growth:+.1f}%)"
            print(f"{month:<12} {count:<12}{growth_str}")
            previous_bookings = count
    else:
        print("  No booking data available yet. Book a flight to see trends.")

    # Additional statistics
    print("\n--- Key Statistics ---")
    _print_traffic_statistics(flights_2d, integrated_data)
    print()


def _print_traffic_statistics(flights_2d, integrated_data):
    """Print airport with highest traffic and most popular destination."""
    airport_traffic = defaultdict(int)
    destination_totals = defaultdict(int)

    for record in integrated_data:
        airport_traffic[record["airport_name"]] += record["passengers"]
        destination_totals[record["destination"]] += record["passengers"]

    if airport_traffic:
        top_airport = max(airport_traffic.items(), key=lambda x: x[1])
        print(f"  Airport with highest traffic: {top_airport[0]} ({top_airport[1]} passengers)")

    if destination_totals:
        top_dest = max(destination_totals.items(), key=lambda x: x[1])
        print(f"  Most popular destination: {top_dest[0]} ({top_dest[1]} passengers)")

    total_passengers = sum(int(row[3]) for row in flights_2d if len(row) >= 4)
    print(f"  Total passengers across all flights: {total_passengers}")


def full_statistics_report(airports_2d, flights_2d, bookings, integrated_data):
    """Comprehensive statistics using integrated dataset."""
    print_header("COMPREHENSIVE TRAVEL STATISTICS")

    airport_traffic = defaultdict(int)
    destination_totals = defaultdict(int)

    for record in integrated_data:
        airport_traffic[record["airport_name"]] += record["passengers"]
        destination_totals[record["destination"]] += record["passengers"]

    if airport_traffic:
        top_airport = max(airport_traffic.items(), key=lambda x: x[1])
        print(f"Airport with highest traffic: {top_airport[0]} ({top_airport[1]} passengers)")

    if destination_totals:
        top_dest = max(destination_totals.items(), key=lambda x: x[1])
        print(f"Most popular destination: {top_dest[0]} ({top_dest[1]} passengers)")

    categories = categorize_flights(flights_2d)
    print(f"Domestic flights: {len(categories.get(FLIGHT_DOMESTIC, []))}")
    print(f"International flights: {len(categories.get(FLIGHT_INTERNATIONAL, []))}")
    print(f"Total airports: {len(airports_2d)}")
    print(f"Total flights: {len(flights_2d)}")
    print(f"Total bookings: {len(bookings)}")
    print()


def prompt_sort_option():
    """Ask user which sort key to use for integrated report."""
    print("\nSort options:")
    print("  1. Passenger count (highest first)")
    print("  2. Airport name (A-Z)")
    print("  3. Destination (A-Z)")
    print("  4. No sorting")
    choice = input("Select sort option (1-4): ").strip()
    if choice == "1":
        return SORT_BY_PASSENGERS, True
    if choice == "2":
        return SORT_BY_AIRPORT, False
    if choice == "3":
        return SORT_BY_DESTINATION, False
    return None, False
