import sys
from datetime import datetime
from transit.constants import City,DayOfWeek,get_city_from_label

# We no longer need load_connections_from_csv here, the manager does it.
from transit.services.station_network_manager import StationNetworkManager
from transit.models.Ticket import Ticket
from transit.models.Trip import Trip
from transit.services.booking_service import BookingService
from typing import List, Dict

# --- Global In-Memory Storage ---
# As per PDF, load data into working memory
try:
    # --- EDITED SECTION ---
    # The StationNetworkManager class you provided expects the file path
    # and handles loading the connections itself.
    print("Hello")
    FILE_PATH = "backend/transit/data/eu_rail_network.csv"
    NETWORK_MANAGER = StationNetworkManager(FILE_PATH)
    # We no longer load ALL_CONNECTIONS here.
    # --- END EDITED SECTION ---
    
    BOOKING_SERVICE = BookingService()
except FileNotFoundError:
    print(f"Error: '{FILE_PATH}' not found.")
    print("Please make sure the data file is in the correct location.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred during initialization: {e}")
    sys.exit(1)
# ---------------------------------


def get_city_input(prompt: str) -> City:
    """Helper to get and validate a city enum from user input."""
    while True:
        city_name = input(prompt)
        city_enum = get_city_from_label(city_name)
        if city_enum:
            return city_enum
        else:
            print(f"Invalid city: '{city_name}'. Please try again.")

def get_day_of_week_input() -> DayOfWeek:
    """Helper to get and validate a DayOfWeek enum from user input."""
    while True:
        date_str = input("Enter departure date (YYYY-MM-DD): ")
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            # .weekday() is Mon=0...Sun=6
            # Our enum is Sun=0...Sat=6
            day_val = (date_obj.weekday() + 1) % 7
            return DayOfWeek(day_val)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_traveller_details() -> List[Dict]:
    """Helper to get details for one or more travellers."""
    travellers = []
    while True:
        try:
            num_str = input("How many travellers (e.g., 1, 2, 3)? ")
            num = int(num_str)
            if num <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive number.")
    
    for i in range(num):
        print(f"\n--- Traveller {i+1} ---")
        name = input("  Name (First and Last): ").strip()
        age_str = input("  Age: ").strip()
        client_id = input("  ID (e.g., Passport Number): ").strip()
        
        if not name or not age_str or not client_id:
            print("All fields are required. Please start over for this traveller.")
            # In a real app, we'd loop this specific traveller
            return get_traveller_details() # Simple restart
        
        try:
            age = int(age_str)
            if age <= 0: raise ValueError
            travellers.append({"name": name, "age": age, "id": client_id})
        except ValueError:
            print("Invalid age. Please start over for this traveller.")
            return get_traveller_details() # Simple restart
            
    return travellers

def run_book_trip():
    """
    Handles Use Case: Book a Trip
    1. Search, 2. Identify, 3. Select, 4. Book
    """
    print("\n--- 1. Search for Connections ---")
    #from_city = get_city_input("Enter departure city (e.g., Montreal): ")
    #to_city = get_city_input("Enter arrival city (e.g., Berlin): ")
    #day = get_day_of_week_input()

    # 1. SEARCH
    #found_trips = NETWORK_MANAGER.dfs_all_paths(from_city, to_city, day)
    found_tickets = NETWORK_MANAGER.dfs_all_paths(City.PARIS, City.BERLIN, DayOfWeek.Friday)
    # --- END EDITED SECTION ---
    
    if not found_tickets:
        print("\nSorry, no trips were found matching your criteria.")
        return

    # 2. IDENTIFY
    print(f"\n--- 2. Found {len(found_tickets)} Possible Trips ---")
    # Sort by duration, then stops
    found_tickets.sort(key=lambda t: (t.total_travel_duration, t.num_connections))
    
    ticket_map: Dict[str, Trip] = {}
    for i, ticket in zip(range(1,len(found_tickets)+1), found_tickets):
        ticket_map[i] = ticket
        print(f"\nOPTION: [{i}]")
        print(ticket) # Use the ticket's __str__ method

    # 3. SELECT
    print("\n--- 3. Select a Ticket ---")
    while True:
        try:            
            selected_id = int(input("Enter the Ticket ID [e.g., 1] you want to book: ").upper().strip())
        except ValueError:
            print("Invalid Ticket ID. Please try again")
        if selected_id in ticket_map:
            selected_ticket = ticket_map[selected_id]
            print(f"You selected:\n{selected_ticket}")
            break
        else:
            print("Invalid Trip ID. Please try again.")

    # 4. BOOK
    print("\n--- 4. Enter Traveller Details ---")
    travellers = get_traveller_details()
    
    # Pass to booking service
    booked_trip = BOOKING_SERVICE.book_trip(selected_ticket, travellers)
    
    print("\n--- Booking Confirmed! ---")
    print("Your trip has been booked with the following tickets:")
    for ticket in booked_trip.tickets:
        print(f"  - {ticket}")

def run_view_trips():
    """
    Handles Use Case: View Trips
    """
    print("\n--- View Your Trips ---")
    client_id = input("Enter your ID (e.g., Passport Number): ").strip()
    last_name = input("Enter your last name: ").strip()

    if not client_id or not last_name:
        print("Both ID and last name are required.")
        return
        
    found_trips = BOOKING_SERVICE.find_trips_for_client(client_id, last_name)
    
    if not found_trips:
        print("\nNo trips found for that client ID and last name.")
        return

    print(f"\n--- Found {len(found_trips)} Trip(s) ---")
    
    # Per PDF, separate into "current" and "past"
    # Note: This is complex without real dates, so we'll just list them.
    # In a real app, we'd compare the trip's date with today's date.
    
    print("\n--- All Booked Trips ---")
    for trip in found_trips:
        print(trip)
        for ticket in trip.tickets:
            print(f"  - {ticket}")
        print("-" * 20) # Separator

def main_loop():
    """
    The main console loop for the user.
    """
    print("==========================================")
    print("  Welcome to the Console Booking System")
    print("==========================================")
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Book a Trip")
        print("2. View My Trips")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            run_book_trip()
        elif choice == '2':
            run_view_trips()
        elif choice == '3':
            print("\nThank you for using the booking system. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_loop()

