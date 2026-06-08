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