# Airtool 
# 62404051 | Muhammad Abdullah Farooqui
# BOCP Final Project 
"""
airport.py - Airport class for AirTool application.
Represents an airport with its core attributes.
"""


class Airport:
    """Represents an airport in the AirTool system."""

    def __init__(self, airport_id, name, country, city, terminal_count):
        """
        Initialize an Airport object.

        Args:
            airport_id: Unique identifier for the airport
            name: Full name of the airport
            country: Country where airport is located
            city: City where airport is located
            terminal_count: Number of terminals at the airport
        """
        self.airport_id = airport_id
        self.name = name
        self.country = country
        self.city = city
        self.terminal_count = terminal_count

    def display_info(self):
        """Display formatted airport information to the console."""
        print(f"  ID:       {self.airport_id}")
        print(f"  Name:     {self.name}")
        print(f"  Country:  {self.country}")
        print(f"  City:     {self.city}")
        print(f"  Terminals:{self.terminal_count}")

    def get_summary(self):
        """Return a one-line summary string for the airport."""
        return (
            f"{self.name} ({self.city}, {self.country}) - "
            f"{self.terminal_count} terminal(s)"
        )

    @classmethod
    def from_row(cls, row):
        """
        Create an Airport object from a CSV row (list of strings).

        Args:
            row: [airport_id, name, country, city, terminal_count]
        """
        return cls(
            airport_id=int(row[0]),
            name=row[1].strip(),
            country=row[2].strip(),
            city=row[3].strip(),
            terminal_count=int(row[4]),
        )

    def to_row(self):
        """Convert Airport object to a list for 2D storage."""
        return [
            str(self.airport_id),
            self.name,
            self.country,
            self.city,
            str(self.terminal_count),
        ]
