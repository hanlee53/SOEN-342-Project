# graph class
from .route_loader import read_csv
from transit.models.Station import Station

from transit.constants import City, DayOfWeek
from transit.models.Connection import Connection
from transit.models.Ticket import Ticket

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
                all_paths.append(Ticket(path_so_far))
                continue
            
            current_station = self.getStation(current_city)
            
            # start_city - connection - stop - connection - stop - connection - end_City
            # limit to max 2 stops (3 connections)
            if len(path_so_far) >= 3 or current_station.outgoing_connections.get(day_of_week) is None:
                continue
            
            # explore all neighbouring connections
            for next_city, connections in current_station.outgoing_connections.get(day_of_week).items():
                for connection in connections:
                    if connection not in path_so_far:  # avoid cycles
                        # ensure chronological order, passenger can make it to the next connection
                        if(connection.arrival_time > path_so_far[-1].arrival_time if path_so_far else True):
                            stack.append((next_city, path_so_far + [connection]))
            
        return all_paths
            
            
            
    
            
