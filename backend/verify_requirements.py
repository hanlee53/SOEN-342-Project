import os
import django
import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from transit.models.Trip import Trip
from transit.models.Ticket import Ticket, TripOption
from transit.models.Connection import Connection
from transit.services.booking_service import BookingService
from transit.services.station_network_manager import StationNetworkManager
from transit.models.Station import Station
from transit.constants import City, DayOfWeek

def verify_trip_id():
    print("\n--- Verifying Numerical Trip ID ---")
    
    # Clear DB
    Ticket.objects.all().delete()
    Trip.objects.all().delete()
    from transit.models.Client import Client
    Client.objects.all().delete()
    
    service = BookingService()
    
    # Create dummy trip option
    c1 = Connection("R1", "Berlin", "Paris", "10:00", "12:00", "Daily", "AVE", "100", "50")
    trip_option = TripOption([c1])
    travellers = [{"id": "ID_TEST", "first_name": "Test", "last_name": "User", "age": 25}]
    
    # Book
    trip = service.book_trip(trip_option, travellers, 1)
    
    print(f"Booked Trip ID: {trip.trip_id} (Type: {type(trip.trip_id)})")
    
    if isinstance(trip.trip_id, int):
        print("SUCCESS: Trip ID is an integer.")
    else:
        print(f"FAILURE: Trip ID is {type(trip.trip_id)}, expected int.")
        
    # Verify in DB
    db_trip = Trip.objects.get(trip_id=trip.trip_id)
    if isinstance(db_trip.trip_id, int):
        print("SUCCESS: DB Trip ID is an integer.")
    else:
        print("FAILURE: DB Trip ID is not an integer.")

def verify_layover_policy():
    print("\n--- Verifying Layover Policy ---")
    
    # Mock StationNetworkManager
    manager = StationNetworkManager("./transit/data/eu_rail_network.csv")
    
    # We will mock the stations and connections to test specific times.
    # Path: A -> B -> C
    # Leg 1: A -> B
    # Leg 2: B -> C (Layover at B)
    
    city_a = City.BERLIN
    city_b = City.PARIS
    city_c = City.LYON
    day = DayOfWeek.Monday
    
    # Helper to create connection
    def create_conn(route, start, end, dep, arr):
        return Connection(route, start.value, end.value, dep, arr, "Daily", "AVE", "10", "10")

    # Scenario 1: Day Layover (1h) - Should Pass
    # A->B: 10:00 - 12:00
    # B->C: 13:00 - 15:00
    # Layover: 1h (Day)
    print("Test 1: Day Layover (1h) - Expect Pass")
    c1 = create_conn("R1", city_a, city_b, "10:00", "12:00")
    c2 = create_conn("R2", city_b, city_c, "13:00", "15:00")
    
    # Mock stations
    station_a = Station(city_a)
    station_a.outgoing_connections = {day: {city_b: [c1]}}
    
    station_b = Station(city_b)
    station_b.outgoing_connections = {day: {city_c: [c2]}}
    
    station_c = Station(city_c)
    station_c.outgoing_connections = {day: {}}
    
    stations = {city_a: station_a, city_b: station_b, city_c: station_c}
    manager.getStation = lambda city: stations.get(city)
    
    paths = manager.dfs_all_paths(city_a, city_c, day)
    if len(paths) == 1:
        print("PASS: Found path with 1h day layover.")
    else:
        print(f"FAIL: Expected 1 path, found {len(paths)}.")

    # Scenario 2: Day Layover (3h) - Should Fail
    # A->B: 10:00 - 12:00
    # B->C: 15:01 - 17:00
    # Layover: 3h 1m (Day)
    print("Test 2: Day Layover (3h) - Expect Fail")
    c2_long = create_conn("R2", city_b, city_c, "15:01", "17:00")
    station_b.outgoing_connections = {day: {city_c: [c2_long]}}
    
    paths = manager.dfs_all_paths(city_a, city_c, day)
    if len(paths) == 0:
        print("PASS: No path found (layover too long).")
    else:
        print(f"FAIL: Expected 0 paths, found {len(paths)}.")

    # Scenario 3: Night Layover (20m) - Should Pass
    # A->B: 22:00 - 23:00 (Arrive at night)
    # B->C: 23:20 - 00:20
    # Layover: 20m (Night)
    print("Test 3: Night Layover (20m) - Expect Pass")
    c1_night = create_conn("R1", city_a, city_b, "22:00", "23:00")
    c2_night = create_conn("R2", city_b, city_c, "23:20", "00:20")
    
    station_a.outgoing_connections = {day: {city_b: [c1_night]}}
    station_b.outgoing_connections = {day: {city_c: [c2_night]}}
    
    paths = manager.dfs_all_paths(city_a, city_c, day)
    if len(paths) == 1:
        print("PASS: Found path with 20m night layover.")
    else:
        print(f"FAIL: Expected 1 path, found {len(paths)}.")

    # Scenario 4: Night Layover (40m) - Should Fail
    # A->B: 22:00 - 23:00
    # B->C: 23:41 - 00:41
    # Layover: 41m (Night)
    print("Test 4: Night Layover (40m) - Expect Fail")
    c2_night_long = create_conn("R2", city_b, city_c, "23:41", "00:41")
    station_b.outgoing_connections = {day: {city_c: [c2_night_long]}}
    
    paths = manager.dfs_all_paths(city_a, city_c, day)
    if len(paths) == 0:
        print("PASS: No path found (night layover too long).")
    else:
        print(f"FAIL: Expected 0 paths, found {len(paths)}.")

if __name__ == "__main__":
    verify_trip_id()
    verify_layover_policy()
