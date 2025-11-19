import os
import django
import sys
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from transit.models.Client import Client
from transit.models.Trip import Trip
from transit.models.Ticket import Ticket, TripOption
from transit.models.Connection import Connection
from transit.services.booking_service import BookingService
from transit.constants import City, DayOfWeek

def verify():
    print("Starting verification...")
    
    # Clear DB for clean test
    Ticket.objects.all().delete()
    Trip.objects.all().delete()
    Client.objects.all().delete()
    
    service = BookingService()
    
    # 1. Create Client
    print("Creating client...")
    client = service.get_or_create_client("ID123", "John", "Doe", 30)
    assert Client.objects.count() == 1
    assert client.first_name == "John"
    assert client.last_name == "Doe"
    print("Client created successfully.")
    
    # 2. Create a Mock TripOption
    # We need connections. Let's mock them or use real ones if we can load them.
    # But loading takes time. Let's mock a connection.
    # Connection __init__ parses strings.
    # route_id, dep_city, arr_city, dep_time, arr_time, days, type, p1, p2
    print("Creating mock trip option...")
    c1 = Connection("R1", "Berlin", "Paris", "10:00", "12:00", "Daily", "AVE", "100", "50")
    trip_option = TripOption([c1])
    
    # 3. Book Trip
    print("Booking trip...")
    travellers = [{"id": "ID123", "first_name": "John", "last_name": "Doe", "age": 30}]
    day = 1 # Monday
    booked_trip = service.book_trip(trip_option, travellers, day)
    
    assert Trip.objects.count() == 1
    assert Ticket.objects.count() == 1
    ticket = Ticket.objects.first()
    assert ticket.client == client
    assert ticket.trip == booked_trip
    assert ticket.route_ids == "R1"
    print("Trip booked successfully.")
    
    # 4. Verify Persistence (Simulated by querying again)
    print("Verifying persistence...")
    trips = service.view_trips("ID123", "Doe")
    assert len(trips) == 1
    assert trips[0].trip_id == booked_trip.trip_id
    print("Persistence verified.")
    
    # 5. Verify Duplicate Prevention (Same booking)
    print("Verifying duplicate prevention (same booking)...")
    try:
        service.book_trip(trip_option, travellers + travellers, day)
        print("FAILED: Should have raised ValueError for duplicate in same booking.")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    # 6. Verify Duplicate Prevention (Global)
    print("Verifying duplicate prevention (global)...")
    try:
        service.book_trip(trip_option, travellers, day)
        print("FAILED: Should have raised ValueError for global duplicate.")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    # 7. Verify Non-Duplicate (Different day)
    print("Verifying non-duplicate (different day)...")
    try:
        service.book_trip(trip_option, travellers, 2) # Tuesday
        print("Success: Booked on different day.")
    except ValueError as e:
        print(f"FAILED: Should allow different day. Error: {e}")

    print("\nALL TESTS PASSED!")

if __name__ == "__main__":
    verify()
