# Airtool 
# 62404051 | Muhammad Abdullah Farooqui
# BOCP Final Project 
"""
utils.py - Helper functions for AirTool application.
Provides formatting, validation, sorting, and display utilities.
"""

# Application constants
APP_NAME = "AirTool - Airport Flight Information & Travel Analytics System"
APP_VERSION = "1.0"
MENU_WIDTH = 60

# File path constants
AIRPORTS_FILE = "airports.csv"
FLIGHTS_FILE = "flights.csv"
BOOKINGS_FILE = "user_bookings.txt"

# Sort option constants
SORT_BY_PASSENGERS = "passengers"
SORT_BY_AIRPORT = "airport"
SORT_BY_DESTINATION = "destination"

# Flight type constants
FLIGHT_DOMESTIC = "Domestic"
FLIGHT_INTERNATIONAL = "International"


def print_header(title):
    """Print a formatted header with the given title."""
    print("\n" + "=" * MENU_WIDTH)
    print(title.center(MENU_WIDTH))
    print("=" * MENU_WIDTH)


def print_separator(char="-"):
    """Print a horizontal separator line."""
    print(char * MENU_WIDTH)


def get_valid_int(prompt, min_val=None, max_val=None):
    """
    Prompt user for a valid integer within optional range.
    Uses try/except for error handling.
    """
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Error: Value must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Error: Value must be at most {max_val}.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid whole number.")


def get_non_empty_string(prompt):
    """Prompt user for a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: Input cannot be empty. Please try again.")


def pause():
    """Wait for user to press Enter before continuing."""
    input("\nPress Enter to continue...")


def format_table_row(columns, widths):
    """Format a row of columns with specified widths."""
    row_parts = []
    for col, width in zip(columns, widths):
        row_parts.append(str(col).ljust(width)[:width])
    return "  ".join(row_parts)


def sort_records(records, sort_key, reverse=False):
    """
    Sort a list of record dictionaries by the given key.
    Supports passengers (int), airport (str), destination (str).
    """
    if sort_key == SORT_BY_PASSENGERS:
        return sorted(records, key=lambda r: r.get("passengers", 0), reverse=True)
    if sort_key == SORT_BY_AIRPORT:
        return sorted(records, key=lambda r: r.get("airport_name", "").lower(), reverse=reverse)
    if sort_key == SORT_BY_DESTINATION:
        return sorted(records, key=lambda r: r.get("destination", "").lower(), reverse=reverse)
    return records


def categorize_flights(flights_2d, flight_type_index=4):
    """
    Group flight records (2D list) by Domestic and International.
    Returns dict with keys 'Domestic' and 'International'.
    """
    categories = {FLIGHT_DOMESTIC: [], FLIGHT_INTERNATIONAL: []}
    for row in flights_2d:
        ftype = row[flight_type_index].strip()
        if ftype in categories:
            categories[ftype].append(row)
        else:
            categories.setdefault(ftype, []).append(row)
    return categories


def parse_month(date_str):
    """Extract YYYY-MM from a date string like 2025-10-01."""
    try:
        parts = date_str.strip().split("-")
        if len(parts) >= 2:
            return f"{parts[0]}-{parts[1]}"
    except (AttributeError, IndexError):
        pass
    return "Unknown"
