

from transit.constants import City, city_from_raw, DayOfWeek, day_name_to_enum, train_type_from_raw as train
from datetime import datetime, timedelta
from typing import Set 

# This class basically represents a single row in the CSV file
# It holds all the information about a single train connection
# It also parses and converts the raw data into more useful formats


class Connection:
    dummy_date = datetime(2000, 1, 1)
    
    def __init__(
        self,
        route_id: str,
        departure_city: str,
        arrival_city: str,
        departure_time: str,
        arrival_time: str,
        days_of_operation: str,
        train_type: str,
        first_class_price: str,
        second_class_price: str
        ):
        self.route_id = route_id
        self.departure_city = city_from_raw[departure_city.lower()]
        self.arrival_city = city_from_raw[arrival_city.lower()]
        hour, minute = map(int, departure_time.split(":"))
        self.departure_time = Connection.dummy_date.replace(hour=hour, minute=minute)
        self.parse_set_arrival_time(arrival_time)
        self.duration = self.arrival_time - self.departure_time
        self.train_type = train[train_type]
        self.first_class_price = float(first_class_price)
        self.second_class_price = float(second_class_price)
        self.days_of_operation = self.parse_days_of_operation(days_of_operation)
        
      
    
    def parse_set_arrival_time(self, arrival_time: str):
        parts = arrival_time.split(" ")
        
        if len(parts) > 1:
              # Arrival time includes day offset, e.g., "23:45 (+1d)"
            time = parts[0]
            day_offset_str = parts[1]
            
            import re
            m = re.match(r"\(\+(\d+)d\)", day_offset_str)
            
            if not m:
                raise ValueError(f"Invalid day offset format: {day_offset_str}")
            
            self.day_offset = int(m.group(1))    
            hour, minute = map(int, time.split(":"))
        else:
            # No day offset, arrival on same dummy date
            self.day_offset = 0
            hour, minute = map(int, arrival_time.split(":"))
            
            
        
        self.arrival_time = (Connection.dummy_date + timedelta(days=self.day_offset)).replace(hour=hour, minute=minute)
    
    def parse_days_of_operation(self, days_of_operation: str) -> Set[DayOfWeek]:
        days = set()
        
        if days_of_operation == "Daily":
            # add all days of the week
            for day in DayOfWeek:
                days.add(day)
        elif( "-" in days_of_operation):
            # add the range of days
            start_str, end_str = days_of_operation.split("-")
            start_day = day_name_to_enum[start_str].value
            end_day = day_name_to_enum[end_str].value
            current_day = start_day
            
            while True:
                days.add(DayOfWeek(current_day))
                if current_day == end_day:
                    break
                current_day = (current_day+1) % 7  # wrap around using modulo
        else:
            # add individual days
            for day_str in days_of_operation.split(","):
                day = day_name_to_enum[day_str.strip()]
                days.add(day)
                
        return days