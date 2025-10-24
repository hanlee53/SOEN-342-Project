import uuid
from typing import List, Dict, Tuple

from transit.models.Client import Client
from transit.models.Trip import Trip
from transit.models.Ticket import Ticket
import copy

class BookingService:
    """
    Manages all logic for booking trips and viewing past trips.
    This service holds the "in-memory" database of all clients
    and all booked trips.
    """
    def __init__(self):
        # "the system maintains records of all clients"
        self._clients: Dict[str, Client] = {} # Key: client_id
        
        # "system maintains records of all... trips"
        self._booked_trips: Dict[str, Trip] = {} # Key: trip_id

    def get_or_create_client(self, client_id: str, name: str, age: int) -> Client:
        """Finds a client by their ID or creates a new one."""
        if client_id not in self._clients:
            new_client = Client(client_id, name, age)
            self._clients[client_id] = new_client
            print(f"(New client record created for {name})")
        
        # TODO: We could add logic to check if name/age matches,
        # but for now, client_id is the unique source of truth.
        return self._clients[client_id]

    def book_trip(self, selected_ticket: Ticket, traveller_details: List[Dict]) -> Trip:
        """
        Books a selected trip for a list of travellers.
        This implements "Use Case: Book a Trip".
        """
        # "Once created, a trip is assigned a unique alphanumeric ID"
        # Generate a simple alphanumeric ID
        trip_id = f"TR-{uuid.uuid4().hex[:6].upper()}"
        
        new_tickets: List[Ticket] = []
        client_ids_on_this_trip = set()

        # "for a single trip they will have multiple reservations"
        for details in traveller_details:
            client = self.get_or_create_client(
                client_id=details['id'],
                name=details['name'],
                age=details['age']
            )

            # "a client may only have a single reservation under their name"
            # This checks for the "no double booking" rule.
            if client.client_id in client_ids_on_this_trip:
                raise ValueError(
                    f"Error: Client {client.name} (ID: {client.client_id}) "
                    f"is already booked on this trip. Cannot add them twice."
                )
            client_ids_on_this_trip.add(client.client_id)

            # "A ticket documents each reservation"
            new_ticket = copy.copy(selected_ticket)
            new_ticket.set_client(client)
            new_tickets.append(new_ticket)

        # Finalize the booking:
        # 1. Update the Trip object with its new ID and tickets
        new_trip = Trip(new_tickets,trip_id)
        
        # 2. Store the booked trip in our "database"
        self._booked_trips[trip_id] = new_trip
        
        print(f"\nSuccessfully booked Trip {trip_id} for {len(new_tickets)} passenger(s).")
        return new_trip

    def view_trips(self, client_id: str, last_name: str) -> List[Trip]:
        """
        Finds all trips for a specific client.
        This implements "Use Case: View Trips".
        """
        # 1. Find the client in our "database"
        client = self._clients.get(client_id)

        # 2. Validate client exists and last name matches
        if not client:
            raise ValueError("No client found with that ID.")
        
        if last_name.lower() not in client.name.lower():
            raise ValueError("Last name does not match the ID provided.")

        # 3. Find all tickets associated with this client
        found_trips = []
        # We must iterate through all booked trips and all their tickets
        for trip in self._booked_trips.values():
            for ticket in trip.tickets:
                if ticket.client.client_id == client_id:
                    found_trips.append(trip)
                    break # Move to the next trip
        
        return found_trips

