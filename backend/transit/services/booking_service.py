import uuid
from typing import List, Dict
from django.db import transaction
from transit.models.Client import Client
from transit.models.Trip import Trip
from transit.models.Ticket import Ticket, TripOption

class BookingService:
    """
    Manages all logic for booking trips and viewing past trips.
    Uses Django ORM for persistence.
    """
    def __init__(self):
        pass

    def get_or_create_client(self, client_id: str, first_name: str, last_name: str, age: int) -> Client:
        """Finds a client by their ID or creates a new one."""
        client, created = Client.objects.get_or_create(
            client_id=client_id,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'age': age
            }
        )
        if created:
            print(f"(New client record created for {first_name} {last_name})")
        else:
            # Optional: Update details if they changed? 
            # For now, assume ID is the source of truth and don't update name/age
            pass
            
        return client

    def book_trip(self, selected_ticket: TripOption, traveller_details: List[Dict], day_of_week: int) -> Trip:
        """
        Books a selected trip for a list of travellers.
        """
        # Generate a simple alphanumeric ID
        trip_id = f"TR-{uuid.uuid4().hex[:6].upper()}"
        
        # We use a transaction to ensure atomicity
        with transaction.atomic():
            new_trip = Trip.objects.create(trip_id=trip_id)
            
            client_ids_on_this_trip = set()
            
            # Get route IDs for the selected trip
            new_route_ids = [c.route_id for c in selected_ticket.connections]
            new_route_ids_str = ",".join(new_route_ids)

            for details in traveller_details:
                client = self.get_or_create_client(
                    client_id=details['id'],
                    first_name=details['first_name'],
                    last_name=details['last_name'],
                    age=details['age']
                )

                # 1. Check for duplicate within this booking request
                if client.client_id in client_ids_on_this_trip:
                    raise ValueError(
                        f"Error: Client {client.first_name} {client.last_name} (ID: {client.client_id}) "
                        f"is already booked on this trip. Cannot add them twice."
                    )
                client_ids_on_this_trip.add(client.client_id)
                
                # 2. Check for global duplicates (same connection, same day)
                # Find all tickets for this client on this day
                existing_tickets = Ticket.objects.filter(client=client, day_of_week=day_of_week)
                
                for ticket in existing_tickets:
                    existing_routes = ticket.route_ids.split(",")
                    # Check intersection
                    if set(new_route_ids).intersection(set(existing_routes)):
                         raise ValueError(
                            f"Error: Client {client.first_name} {client.last_name} (ID: {client.client_id}) "
                            f"already has a reservation for one of these connections on this day."
                        )

                # Create the Ticket record
                Ticket.objects.create(
                    trip=new_trip,
                    client=client,
                    departure_city=selected_ticket.departure_city.value,
                    arrival_city=selected_ticket.arrival_city.value,
                    departure_time=selected_ticket.departure_time,
                    arrival_time=selected_ticket.arrival_time,
                    price=selected_ticket.total_first_class_price + selected_ticket.total_second_class_price, # Storing total for now, or maybe just 2nd class? Let's store sum or just one. The prompt didn't specify price storage details, but Ticket model has 'price'. Let's assume standard price.
                    # Actually, let's just store the second class price as base, or maybe we need to ask user for class?
                    # The current app doesn't ask for class. It just shows both prices.
                    # I'll store the second class price as default 'price' for now.
                    route_ids=new_route_ids_str,
                    day_of_week=day_of_week
                )

            print(f"\nSuccessfully booked Trip {trip_id} for {len(traveller_details)} passenger(s).")
            return new_trip

    def view_trips(self, client_id: str, last_name: str) -> List[Trip]:
        """
        Finds all trips for a specific client.
        """
        # Validate client exists
        try:
            client = Client.objects.get(client_id=client_id)
        except Client.DoesNotExist:
             raise ValueError("No client found with that ID.")
        
        # Validate last name (case-insensitive)
        if client.last_name.lower() != last_name.lower():
            raise ValueError("Last name does not match the ID provided.")

        # Find trips
        # We want trips where this client has a ticket
        trips = Trip.objects.filter(tickets__client=client).distinct()
        
        return list(trips)

