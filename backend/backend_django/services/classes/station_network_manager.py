# graph class
from ..csv_read import read_csv
from .station import Station
from ..enums.city_enum import City
from ..enums.day_of_week_enum import DayOfWeek
from .trip import Trip

class StationNetworkManager:
    def __init__(self):
        self.stations = {}  # key: city name, value: station object
        

    def load_connections(self,file_path: str):
        global connections
        # parse CSV here and populate `connections` list
        
        try:
            print(f"Loading connections from {file_path}...")
            connections = read_csv(file_path)
            print(f"Loaded {len(connections)} connections.")
            
            return connections
        except Exception as e:
            print(f"Error loading connections: {e}")
            return []
            
    def load_network(self,file_path: str):
        self.connections = self.load_connections(file_path)
        
        for connection in self.connections:
            if connection.departure_city not in self.stations:
                self.stations[connection.departure_city] = Station(connection.departure_city)
            
            station = self.stations[connection.departure_city]
            station.add_connection(connection)
            
        list_of_trips = list(self.dfs_all_paths(City.AMSTERDAM, City.EINDHOVEN, DayOfWeek.Saturday))
        
        if(len(list_of_trips) == 0):
            print("No trips found.")
            
        for trip in list_of_trips:
            print(f"Trip from {trip.departure_city.value} to {trip.arrival_city.value} with {len(trip.connections)} connections.\n Total travelling duration: {trip.total_travel_duration}, Total first class price: {trip.total_first_class_price} euro.")
       

            
    def dfs_all_paths(self, start_city : City, end_city :City, day_of_week : DayOfWeek):
        
        all_paths = [] # list of lists of connections
        
        # direct connection check
        # if(self.stations.get(start_city).outgoing_connections.get(day_of_week).get(end_city) is not None):
        #     for connection in self.stations.get(start_city).outgoing_connections.get(day_of_week).get(end_city):
        #         all_paths.append(Trip([connection]))
            
          
        stack = [(start_city, [])]  # (current_city, path_so_far, visited_cities)
        
        while stack:
            
            current_city, path_so_far = stack.pop()
            
            if current_city == end_city and len(path_so_far) <= 3:
                all_paths.append(Trip(path_so_far))
                continue
            
            # limit to max 2 connections (3 legs)
            if len(path_so_far) >= 2 or self.stations.get(current_city).outgoing_connections.get(day_of_week) is None:
                continue
            
            # explore all neighbouring connections
            for next_city, connections in self.stations.get(current_city).outgoing_connections.get(day_of_week).items():
                for connection in connections:
                    if connection not in path_so_far:  # avoid cycles
                        # ensure chronological order, passenger can make it to the next connection
                        if(connection.arrival_time > path_so_far[-1].arrival_time if path_so_far else True):
                            stack.append((next_city, path_so_far + [connection]))
            
        return all_paths
            
            
            
    
            
