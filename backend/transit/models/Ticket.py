from datetime import timedelta
from .Connection import Connection
from .Client import Client

# This class represents a single ticket, which also holds all the
# information about the journey (the list of connections).
# It calculates total travel duration, total price, number of connections, etc.

class Ticket():
    """
    Represents a full trip/journey for a *potential* client.
    The StationNetworkManager will create these objects as search results.
    The BookingService will then assign a client and ticket_id to it.
    """
    # Class-level counter for unique numerical IDs
    _id_counter = 1
    
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
        
        # --- Attributes to be set *after* booking ---
        self.client: Client | None = None
        self.ticket_id: int | None = None # This will be set by BookingService

    def set_client(self, client: Client):
        """
        Assigns a client to this ticket and gives it a unique ID,
        officially "booking" it.
        """
        self.client = client
        # "A ticket has a unique numerical id"
        self.ticket_id = Ticket._id_counter
        Ticket._id_counter += 1
        
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

