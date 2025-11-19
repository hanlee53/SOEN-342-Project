from datetime import timedelta
from .Connection import Connection
from .Client import Client

# This class represents a single ticket, which also holds all the
# information about the journey (the list of connections).
# It calculates total travel duration, total price, number of connections, etc.

from django.db import models
from datetime import timedelta
from .Connection import Connection
from .Client import Client
from .Trip import Trip

# This class represents a single ticket, which also holds all the
# information about the journey (the list of connections).
# It calculates total travel duration, total price, number of connections, etc.

class TripOption:
    """
    Represents a full trip/journey for a *potential* client.
    The StationNetworkManager will create these objects as search results.
    """
    
    def __init__(self, connections: list[Connection]):
        if not connections:
            raise ValueError("Ticket must have at least one connection.")
            
        self.connections = connections
        
        # --- Attributes to fix the sort error in main.py ---
        self.departure_city = connections[0].departure_city
        self.arrival_city = connections[-1].arrival_city
        
        total_duration = timedelta()
        total_first_class_price = 0.0
        total_second_class_price = 0.0
        
        for conn in connections:
            total_duration += conn.duration
            total_first_class_price += conn.first_class_price
            total_second_class_price += conn.second_class_price
            
        self.total_travel_duration = total_duration
        self.total_first_class_price = total_first_class_price
        self.total_second_class_price = total_second_class_price
        
        self.num_connections = len(connections)
        self.is_direct = self.num_connections == 1
        
        self.departure_time = connections[0].departure_time
        self.arrival_time = connections[-1].arrival_time
        # --- End of added attributes ---

    def calculate_transfer_time(self) -> timedelta:
        """
        Calculates the total waiting time *between* connections.
        """
        total_transfer = timedelta()
        # Loop up to the second-to-last connection
        for i in range(len(self.connections) - 1):
            connection_a = self.connections[i]
            connection_b = self.connections[i+1]
            
            wait_time = connection_b.departure_time - connection_a.arrival_time
            
            # Only add if it's a positive wait time
            if wait_time > timedelta():
                total_transfer += wait_time
        return total_transfer

    def __str__(self):
        """
        Provides a human-readable string for the ticket/trip.
        """
        # Create a path string like "City A -> City B -> City C"
        path_start = self.connections[0].departure_city.value
        
        #Get all arrival cities.
        path_arrivals = [conn.arrival_city.value for conn in self.connections]
        
        #Join them all together.
        path = " -> ".join([path_start] + path_arrivals)
        
        # Format duration, removing microseconds
        duration_str = str(self.total_travel_duration).split('.')[0]
        
        stops = "Direct" if self.is_direct else f"{self.num_connections - 1} stop(s)"
        
        return (
            f"Trip: {path} ({stops})\n"
            f"  Duration: {duration_str} | Departs: {self.departure_time.strftime('%H:%M')} | Arrives: {self.arrival_time.strftime('%H:%M')}\n"
            f"  Price (1st): €{self.total_first_class_price:.2f} | Price (2nd): €{self.total_second_class_price:.2f}"
        )

class Ticket(models.Model):
    """
    Represents a booked ticket in the database.
    """
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tickets')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tickets')
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    route_ids = models.TextField() # Comma-separated list of route IDs
    day_of_week = models.IntegerField() # 0=Monday, 6=Sunday (or whatever enum uses)

    def __str__(self):
        return f"Ticket for {self.client} from {self.departure_city} to {self.arrival_city}"

