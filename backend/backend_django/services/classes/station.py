from ..classes.Connection import Connection
from ..enums.city_enum import City

# this class represents a station (node in the graph)
# it holds the city name and a map of outgoing connections
# the outgoing connections are organized by day of week and arrival city

class Station:
    def __init__(self, city: City): 
        self.city = city
        self.outgoing_connections = {}  # key: DayOfWeek, value: map of arrival city to list of connections
        
    def add_connection(self, connection: Connection):
        
        for day_of_week in connection.days_of_operation:
        
            if day_of_week not in self.outgoing_connections:
                self.outgoing_connections[day_of_week] = {}
            
            if connection.arrival_city not in self.outgoing_connections[day_of_week]:
                self.outgoing_connections[day_of_week][connection.arrival_city] = []
                
            self.outgoing_connections[day_of_week][connection.arrival_city].append(connection)
            
        