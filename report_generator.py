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
