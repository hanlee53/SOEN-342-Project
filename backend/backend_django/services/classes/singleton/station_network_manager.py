# graph class
from ...csv_read import read_csv
from ..station import Station
from ...enums.city_enum import City
from ...enums.day_of_week_enum import DayOfWeek
from .. import Connection    
from ..trip import Trip

# implemented the singleton pattern to ensure only one instance of the station network manager exists
# this class loads the railway network from a CSV file and builds the graph representation

class StationNetworkManager:
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StationNetworkManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, file_path: str):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.__connections = []  # list of all connections
        self.__stations = {}  # key: City, value: Station
        self.__load_network(file_path)
        self._initialized = True
        
    
    def getStation(self, city: City):
        return self.__stations.get(city)
    
    def __load_connections(self,file_path: str):
        # parse CSV here and populate `connections` list
        
        try:
            print(f"Loading connections from {file_path}...")
            connections = read_csv(file_path)
            print(f"Loaded {len(connections)} connections.")
            
            return connections
        except Exception as e:
            print(f"Error loading connections: {e}")
            return []
    
    def __load_network(self,file_path: str):
        self.__connections = self.__load_connections(file_path)
        
        for connection in self.__connections:
            # create station if not exists
            if connection.departure_city not in self.__stations:
                self.__stations[connection.departure_city] = Station(connection.departure_city)
            
            # add connection to station
            station = self.__stations[connection.departure_city]
            station.add_connection(connection)
            
        list_of_trips = list(self.dfs_all_paths(City.AMSTERDAM, City.EINDHOVEN, DayOfWeek.Saturday))
        
        if(len(list_of_trips) == 0):
            print("No trips found.")
            
        for trip in list_of_trips:
            print(f"Trip from {trip.departure_city.value} to {trip.arrival_city.value} with {len(trip.connections)} connections.\n Total travelling duration: {trip.total_travel_duration}, Total first class price: {trip.total_first_class_price} euro.")
       

    # finds all paths from start_city to end_city with max 2 connections (3 legs)
    # using depth-first search (DFS)
    # Returns a list of Trip objects
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
            if len(path_so_far) >= 2 or self.__stations.get(current_city).outgoing_connections.get(day_of_week) is None:
                continue
            
            # explore all neighbouring connections
            for next_city, connections in self.__stations.get(current_city).outgoing_connections.get(day_of_week).items():
                for connection in connections:
                    if connection not in path_so_far:  # avoid cycles
                        # ensure chronological order, passenger can make it to the next connection
                        if(connection.arrival_time > path_so_far[-1].arrival_time if path_so_far else True):
                            stack.append((next_city, path_so_far + [connection]))
            
        return all_paths
            
            
            
    
            
